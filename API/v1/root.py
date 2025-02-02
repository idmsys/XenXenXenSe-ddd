from fastapi import APIRouter

from app.settings import Settings

root_router = APIRouter()


@root_router.get("/")
async def v1_root():
    xen_clusters = Settings.get_xen_clusters()
    xen_cluster_names = [xen_cluster for xen_cluster in xen_clusters]

    return {
        "hello": "world",
        "api": {"version": 1, "name": "XenXenXenSe"},
        "clusters": xen_cluster_names,
    }
