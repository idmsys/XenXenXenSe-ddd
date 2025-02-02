from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from starlette.responses import RedirectResponse
from XenAPI.XenAPI import Failure
from XenGarden.GuestMetrics import GuestMetrics
from XenGarden.session import create_session
from XenGarden.VM import VM

from API.v1.Common import xenapi_failure_jsonify
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/guest{url_after:path}")
@router.post("/{cluster_id}/vm/{vm_uuid}/guest{url_after:path}")
@router.put("/{cluster_id}/vm/{vm_uuid}/guest{url_after:path}")
@router.delete("/{cluster_id}/vm/{vm_uuid}/guest{url_after:path}")
@router.patch("/{cluster_id}/vm/{vm_uuid}/guest{url_after:path}")
async def vm_guest(cluster_id: str, vm_uuid: str, url_after: str):
    """Get VM Guest Info"""
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        guest_metrics: GuestMetrics = vm.get_guest_metrics()
        guest_uuid = guest_metrics.get_uuid()

        session.xenapi.session.logout()
        return RedirectResponse(url=f"/v1/{cluster_id}/guest/{guest_uuid}{url_after}")
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
