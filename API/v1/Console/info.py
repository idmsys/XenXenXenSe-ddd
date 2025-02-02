from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenAPI.XenAPI import Failure
from XenGarden.Console import Console
from XenGarden.session import create_session

from API.v1.Common import xenapi_failure_jsonify
from API.v1.Console.serialize import serialize
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/console/{console_uuid}")
async def console_get_by_uuid(
    cluster_id: str,
    console_uuid: str,
):
    """Get Console by UUID"""
    try:
        pass

        session = create_session(
            cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        console: Console = Console.get_by_uuid(session, console_uuid)

        if console is not None:
            ret = dict(success=True, data=await serialize(console))
        else:
            ret = dict(success=False)

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
