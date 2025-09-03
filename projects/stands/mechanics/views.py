from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .services.engine import simulate

def _parse_float(value, default=None):
    try:
        return float(str(value).replace(",", "."))
    except (TypeError, ValueError):
        return default

@login_required
def index(request):
    context = {
        "form": {
            "rpm": "",
            "load": "",
        },
        "errors": {},
        "result": None,
    }

    if request.method == "POST":
        rpm = _parse_float(request.POST.get("rpm"), default=None)
        load = _parse_float(request.POST.get("load"), default=None)

        errors = {}
        if rpm is None or rpm <= 0:
            errors["rpm"] = "Введите положительное число оборотов (rpm)."
        if load is None or not (0 <= load <= 1):
            errors["load"] = "Загрузку указывайте числом от 0.0 до 1.0."

        context["form"]["rpm"] = request.POST.get("rpm", "")
        context["form"]["load"] = request.POST.get("load", "")

        if not errors:
            res = simulate({"rpm": rpm, "load": load})
            context["result"] = res
        else:
            context["errors"] = errors

    return render(request, "stands/mechanics/index.html", context)
