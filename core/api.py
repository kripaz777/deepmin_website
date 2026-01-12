from ninja import NinjaAPI, Schema
from typing import List, Optional
from .models import BlogPost
from django.db.models import Q

api = NinjaAPI()

class BlogPostSchema(Schema):
    title: str
    slug: str
    excerpt: str
    category: str
    created_at: str
    cover_image_url: Optional[str] = None

    @staticmethod
    def resolve_created_at(obj):
        return obj.created_at.strftime("%B %d, %Y")

    @staticmethod
    def resolve_cover_image_url(obj):
        if obj.cover_image:
            return obj.cover_image.url
        return None

@api.get("/posts", response=List[BlogPostSchema])
def list_posts(request, limit: int = 10, offset: int = 0):
    return BlogPost.objects.filter(published=True).order_by('-created_at')[offset:offset+limit]

@api.get("/search", response=List[BlogPostSchema])
def search_posts(request, q: str):
    if not q:
        return []
    return BlogPost.objects.filter(
        Q(title__icontains=q) | Q(content__icontains=q),
        published=True
    )[:5]
