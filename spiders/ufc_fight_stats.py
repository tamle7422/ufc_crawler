'''





'''
import random
import scrapy
from scrapy.loader import ItemLoader
import logging
from scrapy.utils.log import configure_logging
from scrapy_splash import SplashRequest,SplashFormRequest
from ufc_crawler.items import FightSummaryItem,FightStatsItem,EventItem
from ufc_crawler.utils import *
from ..hf_ufc import setFightStatsUrl,setDate,setLocationFightStats,setFightId,setFighterName,setFighterResult, \
    setFighterResultEncode, \
    setFighterUrl,setFighterId,setWeightClass,setDecisionMethod,setFightLastRound,setFightTime,setFightTimeFormat, \
    setFightDetails,setKnockdown,setSigStrikesTotal,setSigStrikesPercentTotal,setStrikesTotal,setTakedown,setTakedownPercent, \
    setSubmissionAttempt,setRev,setTimeControl,setSigStrikes,setSigStrikesPercent,setHeadSigStrikes,setBodySigStrikes, \
    setLegSigStrikes,setDistanceSigStrikes,setClinchSigStrikes,setGroundSigStrikes, \
    setSignificantStrikesTable,setUrlEvent,setLocationEvent,setDateEvent,loadFightStatsItem,loadEventItem, \
    setFighterNameEvent
from ..settings import USER_AGENT_LIST
from .ufc_event import UfcEventScraper
from .ufc_upcoming import UfcUpcomingScraper

# fight details of an event
class UfcFightStatsCrawler(scrapy.Spider):
    name = 'ufc_fight_stats'
    allowed_domains = ["ufcstats.com"]
    start_urls = ['http://ufcstats.com/statistics/events/completed?page=all']

    custom_settings = {
        'ITEM_PIPELINES': {
            # 'ufc_crawler.pipelines.FightSummaryPipeline': 380,
            'ufc_crawler.pipelines.UfcFightStatsPipeline': 375
        },
        "CLOSESPIDER_ITEMCOUNT": 4555
    }

    configure_logging(install_root_handler=False)
    logging.basicConfig(filename='ufc_fight_stats_log.txt',format='%(levelname)s: %(message)s', level=logging.INFO,
        filemode="w+")

    def __init__(self,*args,**kwargs):
        super(UfcFightStatsCrawler,self).__init__(*args,**kwargs)
        self.fightStatsUrlList = []
        self.date = ""
        self.eventName = ""
        self.eventTitle = ""
        self.location = ""
        self.fightId = ""
        self.f1Name = ""
        self.f2Name = ""
        self.f1Id = ""
        self.f2Id = ""
        self.f1Result = ""
        self.f2Result = ""
        self.f1Url = ""
        self.f2Url = ""
        self.f1ResultEncode = ""
        self.f2ResultEncode = ""
        # --------------------------------------------------------------------------------------------------------------
        self.weightClass = ""
        self.decisionMethod = ""
        self.fightLastRound = ""
        self.fightTime = ""
        self.fightTimeFormat = ""
        self.fightDetails = ""
        # --------------------------------------------------------------------------------------------------------------
        self.f1Knockdown = ""
        self.f2Knockdown = ""
        self.f1SigStrikesLandedTotal = ""
        self.f2SigStrikesLandedTotal = ""
        self.f1SigStrikesAttTotal = ""
        self.f2SigStrikesAttTotal = ""
        self.f1SigStrikesPercentTotal = ""
        self.f2SigStrikesPercentTotal = ""
        self.f1StrikesLandedTotal = ""
        self.f2StrikesLandedTotal = ""
        self.f1StrikesAttTotal = ""
        self.f2StrikesAttTotal = ""
        self.f1TakedownLanded = ""
        self.f2TakedownLanded = ""
        self.f1TakedownAtt = ""
        self.f2TakedownAtt = ""
        self.f1TakedownPercent = ""
        self.f2TakedownPercent = ""
        self.f1SubmissionAtt = ""
        self.f2SubmissionAtt = ""
        self.f1Rev = ""
        self.f2Rev = ""
        self.f1TimeControl = ""
        self.f2TimeControl = ""
        self.f1SigStrikesLanded = ""
        self.f2SigStrikesLanded = ""
        self.f1SigStrikesAtt = ""
        self.f2SigStrikesAtt = ""
        self.f1SigStrikesPercent = ""
        self.f2SigStrikesPercent = ""
        self.f1HeadSigStrikesLanded = ""
        self.f2HeadSigStrikesLanded = ""
        self.f1HeadSigStrikesAtt = ""
        self.f2HeadSigStrikesAtt = ""
        self.f1BodySigStrikesLanded = ""
        self.f2BodySigStrikesLanded = ""
        self.f1BodySigStrikesAtt = ""
        self.f2BodySigStrikesAtt = ""
        self.f1LegSigStrikesLanded = ""
        self.f2LegSigStrikesLanded = ""
        self.f1LegSigStrikesAtt = ""
        self.f2LegSigStrikesAtt = ""
        self.f1DistanceSigStrikesLanded = ""
        self.f2DistanceSigStrikesLanded = ""
        self.f1DistanceSigStrikesAtt = ""
        self.f2DistanceSigStrikesAtt = ""
        self.f1ClinchSigStrikesLanded = ""
        self.f2ClinchSigStrikesLanded = ""
        self.f1ClinchSigStrikesAtt = ""
        self.f2ClinchSigStrikesAtt = ""
        self.f1GroundSigStrikesLanded = ""
        self.f2GroundSigStrikesLanded = ""
        self.f1GroundSigStrikesAtt = ""
        self.f2GroundSigStrikesAtt = ""

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
            # parse the event listing page and follow link to individual events page
            # get selector list of event details
            # eventsUrl = response.css('tbody .b-statistics__table-row ::attr(href)')
            # /html/body/section/div/div/div/div[2]/div/table/tbody/tr[1]
            eventsSel = response.xpath( \
                 "/html/body/section/div/div/div/div[2]/div/table/tbody/tr[not(contains(@class,'type_first'))]")
            # eventsUrl1 = response.xpath( \
            #     "..//html/body/section/div/div/div/div[2]/div/table/tbody/tr")

            setFightStatsUrl(self,eventsSel)
            for i in range(0,len(self.fightStatsUrlList)):
                print("num events => {0}".format(i))

                yield SplashRequest(url=self.fightStatsUrlList[i],callback=self.parseEventLink,endpoint="execute",
                     args={"lua_source": self.script},headers={"User-Agent": random.choice(USER_AGENT_LIST)})
                # yield response.follow(eventsUrl1,callback=self.parseEventLink,headers={"User-Agent": random.choice(USER_AGENT_LIST)})

        except Exception as ex:
            print("exception --- error in parse => {0}".format(ex))
            logging.info("exception --- error in parse => {0}".format(ex))

    def parseEventLink(self,response):
        try:
            # parse the event page and follow link to each individual fight page
            # response - event details
            setDate(self,response)
            setLocationFightStats(self,response)

            # grab the fight details html link
            # /html/body/section/div/div/table/tbody/tr[1]/td[1]/p/a
            # fightsUrl = response.xpath("..//html/body/section/div/div/table/tbody/tr/td[1]/p/a")
            fightsUrls = response.xpath("..//html/body/section/div/div/table/tbody/tr/td[1]/p/a/@href").extract()

            for fightUrl in fightsUrls:
                # yield response.follow(fight,callback=self.parseFightStats,cb_kwargs=dict(date=self.date, location=self.location))
                yield SplashRequest(url=fightUrl,callback=self.parseFightStats, endpoint="execute",
                    args={"lua_source": self.script},cb_kwargs=dict(date=self.date,location=self.location),
                    headers={"User-Agent": random.choice(USER_AGENT_LIST)})

        except Exception as ex:
            print("exception --- error in parse event link => {0}".format(ex))
            logging.info("exception --- error in parse event link => {0}".format(ex))

    def parseFightStats(self,response,date,location):
        try:
            # fight details page
            setFightId(self,response)
            setFighterName(self, response)
            setFighterResult(self, response)
            setFighterResultEncode(self, response)
            setFighterUrl(self, response)
            setFighterId(self, response)
            setWeightClass(self, response)
            setDecisionMethod(self, response)
            setFightLastRound(self, response)
            setFightTime(self, response)
            setFightTimeFormat(self, response)
            setFightDetails(self, response)

            checkTable = response.xpath("//table[not(contains(@class,'js-fight-table'))]")

            # fight stats - handle missing values
            if (len(checkTable) == 2):
                # total stats
                setKnockdown(self, response)
                setSigStrikesTotal(self, response)
                setSigStrikesPercentTotal(self, response)
                setStrikesTotal(self,response)
                setTakedown(self,response)
                setTakedownPercent(self,response)
                setSubmissionAttempt(self,response)
                setRev(self,response)
                setTimeControl(self,response)
                # ----------------------------------------------------------------------------------------------------------
                # significant strikes
                setSigStrikes(self,response)
                setSigStrikesPercent(self,response)
                setHeadSigStrikes(self,response)
                setBodySigStrikes(self,response)
                setLegSigStrikes(self,response)
                setDistanceSigStrikes(self,response)
                setClinchSigStrikes(self,response)
                setGroundSigStrikes(self,response)

            # only strikes total table available
            else:
                setSignificantStrikesTable(self)

            loader = loadFightStatsItem(self,response)
            yield loader.load_item()

        except Exception as ex:
            print("exception --- error in parse fight stats => {0}".format(ex))
            logging.info("exception --- error in parse fight stats => {0}".format(ex))

