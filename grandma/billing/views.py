from annoying.decorators import render_to

from .models import Plan


@render_to('upgrade_plan.html')
def upgrade_plan(request):
    plans = Plan.objects.order_by('-id').all()
    return {
        'plans': plans
    }
