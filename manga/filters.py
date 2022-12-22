def custom_queryset_filter(request, queryset):
    type = request.query_params.get("type", None)
    if type:
        queryset = queryset.filter(type__exact=type)
    genres = request.query_params.getlist("genres", None)
    if genres:
        for genre in genres:
            queryset = queryset.filter(genres__in=[genre])
    release_year_min = request.query_params.get("release_year_min", None)
    if release_year_min:
        queryset = queryset.filter(release_year__gte=release_year_min)
    release_year_max = request.query_params.get("release_year_max", None)
    if release_year_max:
        queryset = queryset.filter(release_year__lte=release_year_max)
    return queryset