'''
Define your item pipelines here

# do not forget to add your pipeline to the ITEM_PIPELINES setting
# see: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# define your item pipelines here
# don't forget to add your pipeline to the ITEM_PIPELINES setting
# see: https://docs.scrapy.org/en/latest/topics/item-pipeline.html



'''
import os,re
from sys import platform
from scrapy import signals
from scrapy.exporters import CsvItemExporter,JsonLinesItemExporter
from .items import FightStatsItem,FightSummaryItem,EventItem,EventDetailsItem,UpcomingItem,UpcomingDetailsItem
from datetime import datetime
import pathlib
from ufc_crawler.utils import print_time

class UfcFightStatsPipeline:
    def __init__(self):
        self.fightStatsDir = "csv_files/fight_stats"
        self.fightStatsList = ["fightId","date","location","weightClass","decisionMethod","fightLastRound","fightTime", \
            "fightTimeFormat","fightDetails","f1Name","f1Id","f1Result","f1ResultEncode", \
            "f1Knockdown","f1SigStrikesLandedTotal","f1SigStrikesAttTotal","f1SigStrikesPercentTotal","f1StrikesLandedTotal", \
            "f1StrikesAttTotal","f1TakedownLanded","f1TakedownAtt","f1TakedownPercent","f1SubmissionAtt","f1Rev","f1TimeControl", \
            "f1SigStrikesLanded","f1SigStrikesAtt","f1SigStrikesPercent","f1HeadSigStrikesLanded","f1HeadSigStrikesAtt", \
            "f1BodySigStrikesLanded","f1BodySigStrikesAtt","f1LegSigStrikesLanded","f1LegSigStrikesAtt",
            "f1DistanceSigStrikesLanded","f1DistanceSigStrikesAtt","f1ClinchSigStrikesLanded","f1ClinchSigStrikesAtt", \
            "f1GroundSigStrikesLanded","f1GroundSigStrikesAtt", \
            "f2Name","f2Id","f2Result","f2ResultEncode","f2Knockdown","f2SigStrikesLandedTotal","f2SigStrikesAttTotal",
            "f2SigStrikesPercentTotal","f2StrikesLandedTotal","f2StrikesAttTotal","f2TakedownLanded", \
            "f2TakedownAtt","f2TakedownPercent","f2SubmissionAtt","f2Rev","f2TimeControl","f2SigStrikesLanded", \
            "f2SigStrikesAtt", "f2SigStrikesPercent", "f2HeadSigStrikesLanded","f2HeadSigStrikesAtt", \
            "f2BodySigStrikesLanded","f2BodySigStrikesAtt","f2LegSigStrikesLanded",
            "f2LegSigStrikesAtt","f2DistanceSigStrikesLanded","f2DistanceSigStrikesAtt", "f2ClinchSigStrikesLanded",
            "f2ClinchSigStrikesAtt","f2GroundSigStrikesLanded", "f2GroundSigStrikesAtt"]

        self.fightStatsWriter = ""
        self.fightStatsFileName = ""
        self.fightStatsExporter = ""

    @classmethod
    def from_crawler(cls,crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened,signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed,signals.spider_closed)
        return pipeline

    def spider_opened(self,spider):
        # check system; change if on windows
        if (platform != "linux"):
            self.fightStatsDir = "csv_files\\fight_stats"

        today = datetime.today()
        dt = datetime(today.year,today.month,today.day)
        self.fightStatsFileName = "fight_stats_" + self.checkMonthDay(dt.month) + "_" + self.checkMonthDay(dt.day) + "_"\
            + str(dt.year) + ".csv"

        absolutePathFightStats = os.path.join(os.getcwd(),self.fightStatsDir)
        self.fightStatsWriter = open(os.path.join(absolutePathFightStats,self.fightStatsFileName),'wb+')
        self.fightStatsExporter = CsvItemExporter(self.fightStatsWriter)
        self.fightStatsExporter.fields_to_export = self.fightStatsList
        self.fightStatsExporter.start_exporting()

    def spider_closed(self,spider):
        self.fightStatsExporter.finish_exporting()
        self.fightStatsWriter.close()

    def process_item(self,item,spider):
        if (isinstance(item,FightStatsItem)):
            if (len(item) == 0):
                return item
            else:
                self.fightStatsExporter.export_item(item)
                return item

    def checkMonthDay(self,dayOrMonth):
        if (int(dayOrMonth) <= 9):
            concatStr = "0" + str(dayOrMonth)
            return concatStr
        else:
            return str(dayOrMonth)

class UfcEventPipeline:
    def __init__(self):
        self.eventDir = "csv_files/event"
        self.eventDetailsDir = "csv_files/event_details"
        self.eventList = ["urlEvent","locationEvent","dateEvent"]
        self.eventDetailsList = ["f1Name","f1Result","f1ResultEncode","f1Knockdown","f1Strikes","f1Takedown","f1Submission", \
            "f2Name","f2Result","f2ResultEncode","f2Knockdown","f2Strikes","f2Takedown","f2Submission","dateEventDetails", \
            "locationEventDetails"]

        self.eventWriter = ""
        self.eventFileName = ""
        self.eventExporter = ""
        self.eventDetailsWriter = ""
        self.eventDetailsFileName = ""
        self.eventDetailsExporter = ""

    @classmethod
    def from_crawler(cls,crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened,signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed,signals.spider_closed)
        return pipeline

    def spider_opened(self,spider):
        # check system; change if on windows
        if (platform != "linux"):
            self.eventDir = "csv_files\\event"
            self.eventDetailsDir = "csv_files\\event_details"

        today = datetime.today()
        dt = datetime(today.year,today.month,today.day)
        self.eventFileName = "event_" + self.checkMonthDay(dt.month) + "_" + self.checkMonthDay(dt.day) + "_"\
            + str(dt.year) + ".csv"
        self.eventDetailsFileName = "event_details_" + self.checkMonthDay(dt.month) + "_" + self.checkMonthDay(dt.day) + "_" \
            + str(dt.year) + ".csv"

        absolutePathEvent = os.path.join(os.getcwd(),self.eventDir)
        absolutePathEventDetails = os.path.join(os.getcwd(),self.eventDetailsDir)

        self.eventWriter = open(os.path.join(absolutePathEvent,self.eventFileName),'wb+')
        self.eventExporter = CsvItemExporter(self.eventWriter)
        self.eventExporter.fields_to_export = self.eventList
        self.eventExporter.start_exporting()

        self.eventDetailsWriter = open(os.path.join(absolutePathEventDetails,self.eventDetailsFileName),"wb+")
        self.eventDetailsExporter = CsvItemExporter(self.eventDetailsWriter)
        self.eventDetailsExporter.fields_to_export = self.eventDetailsList
        self.eventDetailsExporter.start_exporting()

    def spider_closed(self,spider):
        self.eventExporter.finish_exporting()
        self.eventWriter.close()

        self.eventDetailsExporter.finish_exporting()
        self.eventDetailsWriter.close()

    def process_item(self,item,spider):
        if (isinstance(item,EventItem)):
            if (len(item) == 0):
                return item
            else:
                self.eventExporter.export_item(item)
                return item

        if (isinstance(item,EventDetailsItem)):
            if (len(item) == 0):
                return item
            else:
                self.eventDetailsExporter.export_item(item)
                return item

    def checkMonthDay(self,dayOrMonth):
        if (int(dayOrMonth) <= 9):
            concatStr = "0" + str(dayOrMonth)
            return concatStr
        else:
            return str(dayOrMonth)

class UfcUpcomingPipeline:
    def __init__(self):
        self.upcomingDir = "csv_files/upcoming"
        self.upcomingDetailsDir = "csv_files/upcoming_details"
        self.upcomingList = ["urlEvent","locationEvent","dateEvent"]
        self.upcomingDetailsList = ["eventNameUpcoming","dateUpcomingDetails","locationUpcomingDetails","f1Name","f2Name", \
            "weightClass"]

        self.upcomingWriter = ""
        self.upcomingFileName = ""
        self.upcomingExporter = ""
        self.upcomingDetailsWriter = ""
        self.upcomingDetailsFileName = ""
        self.upcomingDetailsExporter = ""

    @classmethod
    def from_crawler(cls,crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened,signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed,signals.spider_closed)
        return pipeline

    def spider_opened(self,spider):
        # check system; change if on windows
        if (platform != "linux"):
            self.upcomingDir = "csv_files\\upcoming"
            self.upcomingDetailsDir = "csv_files\\upcoming_details"

        today = datetime.today()
        dt = datetime(today.year,today.month,today.day)
        self.upcomingFileName = "upcoming_" + self.checkMonthDay(dt.month) + "_" + self.checkMonthDay(dt.day) + "_"\
            + str(dt.year) + ".csv"
        self.upcomingDetailsFileName = "upcoming_details_" + self.checkMonthDay(dt.month) + "_" + self.checkMonthDay(dt.day) + "_" \
            + str(dt.year) + ".csv"

        absolutePathUpcoming = os.path.join(os.getcwd(),self.upcomingDir)
        absolutePathUpcomingDetails = os.path.join(os.getcwd(),self.upcomingDetailsDir)

        self.upcomingWriter = open(os.path.join(absolutePathUpcoming,self.upcomingFileName),'wb+')
        self.upcomingExporter = CsvItemExporter(self.upcomingWriter)
        self.upcomingExporter.fields_to_export = self.upcomingList
        self.upcomingExporter.start_exporting()

        self.upcomingDetailsWriter = open(os.path.join(absolutePathUpcomingDetails,self.upcomingDetailsFileName),"wb+")
        self.upcomingDetailsExporter = CsvItemExporter(self.upcomingDetailsWriter)
        self.upcomingDetailsExporter.fields_to_export = self.upcomingDetailsList
        self.upcomingDetailsExporter.start_exporting()

    def spider_closed(self,spider):
        self.upcomingExporter.finish_exporting()
        self.upcomingWriter.close()

        self.upcomingDetailsExporter.finish_exporting()
        self.upcomingDetailsWriter.close()

    def process_item(self,item,spider):
        if (isinstance(item,UpcomingItem)):
            if (len(item) == 0):
                return item
            else:
                self.upcomingExporter.export_item(item)
                return item

        if (isinstance(item,UpcomingDetailsItem)):
            if (len(item) == 0):
                return item
            else:
                self.upcomingDetailsExporter.export_item(item)
                return item

    def checkMonthDay(self,dayOrMonth):
        if (int(dayOrMonth) <= 9):
            concatStr = "0" + str(dayOrMonth)
            return concatStr
        else:
            return str(dayOrMonth)