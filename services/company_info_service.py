from typing import List
from database import (
    key_metrics_collection,
    milestones_collection,
    testimonials_collection,
    awards_collection,
    media_coverage_collection
)

class CompanyInfoService:
    
    @staticmethod
    def get_key_metrics() -> List[dict]:
        """Get current key metrics"""
        metrics = list(key_metrics_collection.find().sort("display_order", 1))
        for metric in metrics:
            metric["id"] = str(metric.pop("_id"))
        return metrics
    
    @staticmethod
    def get_milestones(limit: int = 20) -> List[dict]:
        """Get company milestones"""
        milestones = list(milestones_collection.find().sort("date", -1).limit(limit))
        for milestone in milestones:
            milestone["id"] = str(milestone.pop("_id"))
        return milestones
    
    @staticmethod
    def get_testimonials(featured_only: bool = False) -> List[dict]:
        """Get customer testimonials"""
        query = {"is_featured": True} if featured_only else {}
        testimonials = list(testimonials_collection.find(query).sort("date_added", -1))
        for testimonial in testimonials:
            testimonial["id"] = str(testimonial.pop("_id"))
        return testimonials
    
    @staticmethod
    def get_awards() -> List[dict]:
        """Get company awards"""
        awards = list(awards_collection.find().sort("date_received", -1))
        for award in awards:
            award["id"] = str(award.pop("_id"))
        return awards
    
    @staticmethod
    def get_media_coverage(limit: int = 10) -> List[dict]:
        """Get media coverage"""
        coverage = list(media_coverage_collection.find().sort("publish_date", -1).limit(limit))
        for item in coverage:
            item["id"] = str(item.pop("_id"))
        return coverage
    
    @staticmethod
    def get_executive_summary() -> dict:
        """Get executive summary data"""
        return {
            "metrics": CompanyInfoService.get_key_metrics(),
            "recent_milestones": CompanyInfoService.get_milestones(limit=5),
            "featured_testimonials": CompanyInfoService.get_testimonials(featured_only=True),
            "awards": CompanyInfoService.get_awards(),
            "media_coverage": CompanyInfoService.get_media_coverage(limit=5)
        }
