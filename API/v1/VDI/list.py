import asyncio
from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenAPI.XenAPI import Failure
from XenGarden.session import create_session
from XenGarden.VDI import VDI

from API.v1.Common import xenapi_failure_jsonify
from API.v1.VDI.serialize import serialize
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vdi/list")
async def vdi_list(cluster_id: str):
    """Get VDI by UUID"""
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vdis = VDI.get_all(session=session)
        __vdi_list = await asyncio.gather(*[serialize(vdi) for vdi in vdis])

        if vdis is not None:
            ret = dict(success=True, data=__vdi_list)
        else:
            ret = dict(success=False)

        session.xenapi.session.logout()
        return ret
    except Failure as xenapi_error:
        raise HTTPException(
            status_code=500, detail=xenapi_failure_jsonify(xenapi_error)
        )
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )
    except RemoteDisconnected as rd_error:
        raise HTTPException(status_code=500, detail=rd_error.strerror)
