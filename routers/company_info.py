from fastapi import APIRouter, Depends
from routers.admin_auth import get_current_admin, get_current_user
from services.company_info_service import CompanyInfoService

router = APIRouter(prefix="/api/company", tags=["Company Information"])

@router.get("/executive-summary")
def get_executive_summary(current_user: dict = Depends(get_current_admin)):
    """Get executive summary with key highlights"""
    return CompanyInfoService.get_executive_summary()

@router.get("/metrics")
def get_key_metrics(current_user: dict = Depends(get_current_admin)):
    """Get key company metrics"""
    return CompanyInfoService.get_key_metrics()

@router.get("/milestones")
def get_milestones(current_user: dict = Depends(get_current_admin)):
    """Get company milestones"""
    return CompanyInfoService.get_milestones()

@router.get("/testimonials")
def get_testimonials(
    featured_only: bool = False,
    current_user: dict = Depends(get_current_admin)
):
    """Get customer testimonials"""
    return CompanyInfoService.get_testimonials(featured_only)

@router.get("/awards")
def get_awards(current_user: dict = Depends(get_current_admin)):
    """Get company awards"""
    return CompanyInfoService.get_awards()

@router.get("/media-coverage")
def get_media_coverage(current_user: dict = Depends(get_current_user)):
    """Get media coverage"""
    return CompanyInfoService.get_media_coverage()