import random
import scrapy
from scrapy.loader import ItemLoader
import logging
from scrapy.utils.log import configure_logging
from scrapy_splash import SplashRequest,SplashFormRequest
from ufc_crawler.items import FightSummaryItem,FightStatsItem,EventItem
from ufc_crawler.utils import *
from ..settings import USER_AGENT_LIST
from ..hf_ufc import setDate,setLocationFightStats,setFighterName,setWeightClass,setUrlEvent, \
    setLocationEvent,setDateEvent,loadFightStatsItem,loadUpcomingItem,setDateUpcomingDetails,setLocationUpcomingDetails, \
    setEventNameUpcoming,setFighterNameEvent,setFighterResultEvent, \
    setKnockdownEvent,setStrikesEvent,setTakedownEvent,setSubmissionEvent,setWeightClassEvent,setFightDetailsEvent, \
    setFightLastRoundEvent,setFightTimeEvent,loadUpcomingDetailsItem, \
    checkEmpty

global countUpcomingDetails
countUpcomingDetails = 0

# upcoming events
class UfcUpcomingScraper(scrapy.Spider):
    name = "ufc_upcoming"
    allowed_domains = ["ufcstats.com"]
    start_urls = ['http://ufcstats.com/statistics/events/upcoming']

    custom_settings = {
        'ITEM_PIPELINES': {
            'ufc_crawler.pipelines.UfcUpcomingPipeline': 365,
        },
        "CLOSESPIDER_ITEMCOUNT": 5499
    }

    configure_logging(install_root_handler=False)
    logging.basicConfig(filename='ufc_upcoming_log.txt',format='%(levelname)s: %(message)s',level=logging.INFO,
                        filemode="w+")

    def __init__(self, *args, **kwargs):
        super(UfcUpcomingScraper, self).__init__(*args, **kwargs)
        self.countUpcomingDetails = countUpcomingDetails
        self.urlEventList = ""
        self.dateEventList = ""
        self.locationEventList = ""
        self.eventNameUpcoming = ""
        self.dateUpcomingDetails = ""
        self.locationUpcomingDetails = ""
        self.f1Name = ""
        self.f2Name = ""
        self.f1Result = ""
        self.f2Result = ""
        self.f1ResultEncode = ""
        self.f2ResultEncode = ""
        self.f1Knockdown = ""
        self.f2Knockdown = ""
        self.f1Strikes = ""
        self.f2Strikes = ""
        self.f1Takedown = ""
        self.f2Takedown = ""
        self.f1Submission = ""
        self.f2Submission = ""
        self.weightClass = ""
        self.fightDetails = ""
        self.fightLastRound = ""
        self.fightTime = ""

        self.script = """
                         function main(splash,args)
                             function focus(sel)
                                 splash:select(sel):focus()
                             end

                             local cookies = splash:get_cookies()
                             splash:init_cookies(cookies)
                             assert(splash:go(splash.args.url))

                             focus('input[name=query]')
                             splash:send_text("ufc")
                             assert(splash:wait(1.5))
                             splash:send_keys("<Return>")
                             assert(splash:wait(1.5))

                             return {
                                 cookies,
                                 html = splash:html(),
                                 png = splash:png(),
                                 har = splash:har()
                             }
                         end
                      """

    def parse(self,response):
        try:
            # /html/body/section/div/div/div/div[2]/div/table/tbody/tr[1]
            trTags = response.xpath("..//html/body/section/div/div/div/div[2]/div/table/tbody/tr")

            setUrlEvent(self,trTags)
            setDateEvent(self,trTags)
            setLocationEvent(self,trTags)

            for i in range(0, len(self.urlEventList)):
                loader = loadUpcomingItem(self,response,i)
                yield loader.load_item()

                yield SplashRequest(url=self.urlEventList[i],callback=self.parseUpcomingDetails,endpoint="execute",
                    args={"lua_source": self.script},cb_kwargs=dict(date=self.dateEventList[i],location=self.locationEventList[i]), \
                    headers={"User-Agent": random.choice(USER_AGENT_LIST)})
                # yield scrapy.Request(url=self.urlEvent,callback=self.parseEventDetails, \
                #     headers={"User-Agent":random.choice(USER_AGENT_LIST)})

        except Exception as ex:
            print("exception --- error in parse => {0}".format(ex))
            logging.info("exception --- error in parse => {0}".format(ex))

    def parseUpcomingDetails(self,response,**kwargs):
        try:
            # /html/body/section/div/div/table/tbody/tr[1]
            trTags = checkEmpty(response.xpath("..//html/body/section/div/div/table/tbody/tr[(@data-link)]"))

            setEventNameUpcoming(self,response)
            setDateUpcomingDetails(self,**kwargs)
            setLocationUpcomingDetails(self,**kwargs)

            for i in range(0,len(trTags)):
                print("upcoming details => {0}".format(self.countUpcomingDetails))
                self.countUpcomingDetails += 1
                setFighterNameEvent(self,trTags,i)
                setWeightClassEvent(self, trTags, i)
                loader = loadUpcomingDetailsItem(self, response)
                yield loader.load_item()

        except Exception as ex:
            print("exception --- error in parse upcoming details => {0}".format(ex))
            logging.info("exception --- error in parse upcoming details => {0}".format(ex))
