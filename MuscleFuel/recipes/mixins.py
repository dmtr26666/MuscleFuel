from django.db.models import Value
from django.db.models.functions import Coalesce
from django.db.models import Avg

class RecipeListMixin:
    def get_queryset(self):
        queryset = super().get_queryset()

        if type(self).__name__ == 'SavedRecipesView':
            queryset = queryset.filter(favourited_by__user=self.request.user)
        else:
            queryset = queryset.filter(is_public=True)

        queryset = queryset.annotate(
            average_rating=Coalesce(Avg('reviews__rating'), Value(0.0))  # Replace None with 0
        )

        query = self.request.GET.get('q')

        if query:
            queryset.filter(title__icontains=query)

        sort_by = self.request.GET.get('sort')
        if sort_by == 'protein_desc':
            queryset = queryset.order_by('-protein')
        elif sort_by == 'protein_asc':
            queryset = queryset.order_by('protein')
        elif sort_by == 'calories_desc':
            queryset = queryset.order_by('-calories')
        elif sort_by == 'calories_asc':
            queryset = queryset.order_by('calories')
        elif sort_by == 'rating_desc':
            queryset = queryset.order_by('-average_rating')
        elif sort_by == 'oldest':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset