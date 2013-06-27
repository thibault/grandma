from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag
def analytics_tag():
    if hasattr(settings, 'ANALYTICS_TAG_ID'):
        tag_id = settings.ANALYTICS_TAG_ID
        tag = analytics_code % tag_id
    else:
        tag = ''
    return tag


analytics_code = '''
<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', '%s']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>
'''
