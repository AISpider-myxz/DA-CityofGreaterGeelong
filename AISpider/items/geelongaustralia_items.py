from . import BaseItem
from scrapy import Field


class Geelongaustralia(BaseItem):
    app_num = Field()
    vic_smart = Field()
    lodge_date = Field()

    address = Field()
    description = Field()
    changes_ = Field()
    type_ = Field()

    notice_date = Field()
    authority = Field()

    decision_date = Field()
    decision = Field()

    vc_refno = Field()
    vc_decision = Field()
    vc_date = Field()

    class Meta:
        table = 'geelongaustralia'
        unique_fields = ['app_num', ]
