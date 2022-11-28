import re
from datetime import datetime
from scrapy.loader import ItemLoader
from .items import FightStatsItem,EventItem,EventDetailsItem,UpcomingItem,UpcomingDetailsItem
import logging
# from .switch_month import switchMonthThreeLetters

def setFightStatsUrl(self,eventsSel):
    try:
        # /html/body/section/div/div/div/div[2]/div/table/tbody/tr[3]/td[1]/i/a
        fightStatsUrlList = checkEmpty(eventsSel[1].xpath("..//td[1]/i/a/@href").extract())
        if (fightStatsUrlList != "None"):
            self.fightStatsUrlList = fightStatsUrlList
        else:
            self.fightStatsUrlList = "None"

    except Exception as ex:
        print("exception --- error in set fight stats url => {0}".format(ex))
        self.fightStatsUrlList = "None"


def setDate(self,response):
    try:
        # /html/body/section/div/div/div[1]/ul/li[1]/text()
        date = checkEmpty(response.xpath("..//html/body/section/div/div/div[1]/ul/li[1]/text()").extract()[1].strip())
        if (date != "None"):
            self.date = date.strip()
        else:
            self.date = "None"

    except Exception as ex:
        print("exception --- error in set date => {0}".format(ex))
        self.date = "None"

def setLocationFightStats(self,response):
    try:
        # /html/body/section/div/div/div[1]/ul/li[2]/text()
        location = checkEmpty(response.xpath("..//html/body/section/div/div/div[1]/ul/li[2]/text()")).extract()[1].strip()
        if (location != "None"):
            self.location = location.strip()
        else:
            self.location = "None"

    except Exception as ex:
        print("exception --- error in set location => {0}".format(ex))
        self.location = "None"

def setFightId(self,response):
    try:
        fightId = checkEmpty(response.url.split('/')[-1])
        if (fightId != "None"):
            self.fightId = fightId.strip()
        else:
            self.fightId = "None"

    except Exception as ex:
        print("exception --- error in set fight id => {0}".format(ex))
        self.fightId = "None"

def setFighterResult(self,response):
    try:
        # win and loss
        # /html/body/section/div/div/div[1]/div[1]/i
        fighterResult = checkEmpty(response.xpath("..//html/body/section/div/div/div[1]/div/i/text()").getall())
        if (fighterResult != "None"):
            self.f1Result = fighterResult[0].strip()
            self.f2Result = fighterResult[1].strip()
        else:
            self.f1Result = "None"
            self.f2Result = "None"

    except Exception as ex:
        print("exception --- error in set fighter result => {0}".format(ex))
        self.f1Result = "None"
        self.f2Result = "None"

def setFighterResultEncode(self,response):
    try:
        if (self.f1Result != "None" and self.f2Result != "None"):
            self.f1ResultEncode = "1" if (self.f1Result == "W") else "0"
            self.f2ResultEncode = "1" if (self.f2Result == "W") else "0"
        else:
            self.f1ResultEncode = "None"
            self.f2ResultEncode = "None"

    except Exception as ex:
        print("exception --- error in set fighter result => {0}".format(ex))
        self.f1ResultEncode = "None"
        self.f2ResultEncode = "None"

def setFighterName(self,response):
    try:
        # /html/body/section/div/div/div[1]/div[1]/div/h3/a
        fighterNames = checkEmpty(response.xpath("..//html/body/section/div/div/div[1]/div/div/h3/a/text()").extract())
        if (fighterNames != "None"):
            self.f1Name = fighterNames[0].strip()
            self.f2Name = fighterNames[1].strip()
        else:
            self.f1Name = "None"
            self.f2Name = "None"

    except Exception as ex:
        print("exception --- error in set fighter names => {0}".format(ex))
        self.f1Name = "None"
        self.f2Name = "None"

def setFighterUrl(self,response):
    try:
        # id's - handle errors due to missing fighter link
        # /html/body/section/div/div/div[1]/div[1]/div/h3/a
        urls = checkEmpty(response.xpath("..//html/body/section/div/div/div[1]/div/div/h3/a/@href").getall())
        if (urls != "None"):
            self.f1Url = urls[0].strip()
            self.f2Url = urls[1].strip()
        else:
            self.f1Url = "None"
            self.f2Url = "None"

    except Exception as ex:
        print("exception --- error in set fighter url => {0}".format(ex))
        self.f1Url = "None"
        self.f2Url = "None"

def setFighterId(self,response):
    try:

        if (self.f1Url != "None" and self.f2Url != "None"):
            self.f1Id = self.f1Url.split('/')[-1].strip()
            self.f2Id = self.f2Url.split('/')[-1].strip()
        else:
            self.f1Id = "None"
            self.f2Id = "None"

    except Exception as ex:
        print("exception --- error in set fighter id => {0}".format(ex))
        self.f1Id = "None"
        self.f2Id = "None"

def setWeightClass(self,response):
    try:
        # /html/body/section/div/div/div[2]/div[1]/i
        weightClass = checkEmpty(response.xpath("..//html/body/section/div/div/div[2]/div[1]/i/text()").get())

        if (weightClass != "None" and len(weightClass.strip()) != 0):
            self.weightClass = weightClass.strip()
        else:
            self.weightClass = "None"

    except Exception as ex:
        print("exception --- error in set weight class => {0}".format(ex))
        self.weightClass = "None"

def setDecisionMethod(self,response):
    try:
        # /html/body/section/div/div/div[2]/div[2]/p[1]/i[1]/i[2]
        decisionMethod = response.xpath("..//html/body/section/div/div/div[2]/div[2]/p[1]/i[1]/i[2]/text()").get()
        if (decisionMethod != "None"):
            self.decisionMethod = decisionMethod
        else:
            self.decisionMethod = "None"

    except Exception as ex:
        print("exception --- error in set decision method => {0}".format(ex))
        self.decisionMethod = "None"

def setFightLastRound(self,response):
    try:
        # /html/body/section/div/div/div[2]/div[2]/p[1]/i[2]/text()
        fightLastRound = checkEmpty(response.xpath( \
            "..//html/body/section/div/div/div[2]/div[2]/p[1]/i[2]/text()").extract()[-1].strip())
        if (fightLastRound != "None"):
            self.fightLastRound = fightLastRound
        else:
            self.fightLastRound = "None"

    except Exception as ex:
        print("exception --- error in set fight last round => {0}".format(ex))
        self.fightLastRound = "None"

def setFightTime(self,response):
    try:
        # /html/body/section/div/div/div[2]/div[2]/p[1]/i[3]/text()
        fightTime = checkEmpty(response.xpath( \
            "..//html/body/section/div/div/div[2]/div[2]/p[1]/i[3]/text()").extract()[-1].strip())
        if (fightTime != "None"):
            self.fightTime = fightTime
        else:
            self.fightTime = "None"

    except Exception as ex:
        print("exception --- error in set fight time => {0}".format(ex))
        self.fightTime = "None"

def setFightTimeFormat(self,response):
    try:
        # /html/body/section/div/div/div[2]/div[2]/p[1]/i[4]/text()
        fightTimeFormat = checkEmpty(response.xpath( \
            "..//html/body/section/div/div/div[2]/div[2]/p[1]/i[4]/text()").extract()[-1].strip())
        if (fightTimeFormat != "None"):
            self.fightTimeFormat = fightTimeFormat
        else:
            self.fightTimeFormat = "None"

    except Exception as ex:
        print("exception --- error in set fight time format => {0}".format(ex))
        self.fightTimeFormat = "None"

def setFightDetails(self,response):
    try:
        # /html/body/section/div/div/div[2]/div[2]/p[2]/text()
        fightDetails = checkEmpty(response.xpath( \
            "..//html/body/section/div/div/div[2]/div[2]/p[2]/text()").extract()[-1].strip())
        if (fightDetails != "None"):
            self.fightDetails = re.sub(r"(\n)+","",fightDetails.strip())
        else:
            self.fightDetails = "None"

    except Exception as ex:
        print("exception --- error in set fight details => {0}".format(ex))
        self.fightDetails = "None"

# ----------------------------------------------------------------------------------------------------------------------
def setKnockdown(self, response):
    try:
        # /html/body/section/div/div/section[2]/table/tbody/tr/td[2]/p[1]
        knockdown = checkEmpty(response.xpath("..//html/body/section/div/div/section[2]/table/tbody/tr/td[2]/p/text()").extract())
        if (knockdown != "None"):
            self.f1Knockdown = knockdown[0].strip()
            self.f2Knockdown = knockdown[1].strip()
        else:
            self.f1Knockdown = "None"
            self.f2Knockdown = "None"

    except Exception as ex:
        print("exception --- error in set knockdown => {0}".format(ex))
        self.f1Knockdown = "None"
        self.f2Knockdown = "None"

def setSigStrikesTotal(self, response):
    try:
        # /html/body/section/div/div/section[2]/table/tbody/tr/td[3]/p[1]
        sigStrikesTotal = checkEmpty(response.xpath( \
            "..//html/body/section/div/div/section[2]/table/tbody/tr/td[3]/p/text()").extract())
        if (sigStrikesTotal != "None"):
            f1SigStrikesTotal = sigStrikesTotal[0].strip()
            f2SigStrikesTotal = sigStrikesTotal[1].strip()

            self.f1SigStrikesLandedTotal = f1SigStrikesTotal.split("of")[0].strip()
            self.f1SigStrikesAttTotal = f1SigStrikesTotal.split("of")[1].strip()
            self.f2SigStrikesLandedTotal = f2SigStrikesTotal.split("of")[0].strip()
            self.f2SigStrikesAttTotal = f2SigStrikesTotal.split("of")[1].strip()
        else:
            self.f1SigStrikesLandedTotal = "None"
            self.f1SigStrikesAttTotal = "None"
            self.f2SigStrikesLandedTotal = "None"
            self.f2SigStrikesAttTotal = "None"

    except Exception as ex:
        print("exception --- error in set significant strikes total => {0}".format(ex))
        self.f1SigStrikesLandedTotal = "None"
        self.f1SigStrikesAttTotal = "None"
        self.f2SigStrikesLandedTotal = "None"
        self.f2SigStrikesAttTotal = "None"

def setSigStrikesPercentTotal(self,response):
    try:
        # /html/body/section/div/div/section[2]/table/tbody/tr/td[4]/p[1]
        sigStrikesPercentTotal = checkEmpty(response.xpath( \
            "..//html/body/section/div/div/section[2]/table/tbody/tr/td[4]/p/text()").extract())
        if (sigStrikesPercentTotal != "None"):
            self.f1SigStrikesPercentTotal = sigStrikesPercentTotal[0].strip() if (sigStrikesPercentTotal[0].strip() != "---") else "None"
            self.f2SigStrikesPercentTotal = sigStrikesPercentTotal[1].strip() if (sigStrikesPercentTotal[1].strip() != "---") else "None"

        else:
            self.f1SigStrikesPercentTotal = "None"
            self.f2SigStrikesPercentTotal = "None"

    except Exception as ex:
        print("exception --- error in set significant strikes total => {0}".format(ex))
        self.f1SigStrikesPercentTotal = "None"
        self.f2SigStrikesPercentTotal = "None"

def setStrikesTotal(self,response):
    try:
        # /html/body/section/div/div/section[2]/table/tbody/tr/td[5]/p[1]
        strikesTotal = checkEmpty(response.xpath( \
            "/html/body/section/div/div/section[2]/table/tbody/tr/td[5]/p/text()").extract())
        if (strikesTotal != "None"):
            f1StrikesTotal = strikesTotal[0].strip()
            f2StrikesTotal = strikesTotal[1].strip()

            self.f1StrikesLandedTotal = f1StrikesTotal.split("of")[0].strip()
            self.f1StrikesAttTotal = f1StrikesTotal.split("of")[1].strip()
            self.f2StrikesLandedTotal = f2StrikesTotal.split("of")[0].strip()
            self.f2StrikesAttTotal = f2StrikesTotal.split("of")[1].strip()
        else:
            self.f1StrikesLandedTotal = "None"
            self.f1StrikesAttTotal = "None"
            self.f2StrikesLandedTotal = "None"
            self.f2StrikesAttTotal = "None"

    except Exception as ex:
        print("exception --- error in set strikes total => {0}".format(ex))
        self.f1StrikesLandedTotal = "None"
        self.f1StrikesAttTotal = "None"
        self.f2StrikesLandedTotal = "None"
        self.f2StrikesAttTotal = "None"

def setTakedown(self,response):
    try:
        # /html/body/section/div/div/section[2]/table/tbody/tr/td[6]/p[1]
        takedown = checkEmpty(response.xpath( \
            "..//html/body/section/div/div/section[2]/table/tbody/tr/td[6]/p/text()").extract())
        if (takedown != "None"):
            f1Takedown = takedown[0].strip()
            f2Takedown = takedown[1].strip()

            self.f1TakedownLanded = f1Takedown.split("of")[0].strip()
            self.f1TakedownAtt = f1Takedown.split("of")[1].strip()
            self.f2TakedownLanded = f2Takedown.split("of")[0].strip()
            self.f2TakedownAtt = f2Takedown.split("of")[1].strip()
        else:
            self.f1TakedownLanded = "None"
            self.f1TakedownAtt = "None"
            self.f2TakedownLanded = "None"
            self.f2TakedownAtt = "None"

    except Exception as ex:
        print("exception --- error in set takedown => {0}".format(ex))
        self.f1TakedownLanded = "None"
        self.f1TakedownAtt = "None"
        self.f2TakedownLanded = "None"
        self.f2TakedownAtt = "None"

def setTakedownPercent(self,response):
    try:
        # /html/body/section/div/div/section[2]/table/tbody/tr/td[7]/p[1]
        takedownPercent = checkEmpty(response.xpath( \
            "..//html/body/section/div/div/section[2]/table/tbody/tr/td[7]/p/text()").extract())
        if (takedownPercent != "None"):
            if (takedownPercent[0].strip() != "---"):
                self.f1TakedownPercent = takedownPercent[0].strip()
            else:
                self.f1TakedownPercent = "None"

            if (takedownPercent[1].strip() != "---"):
                self.f2TakedownPercent = takedownPercent[1].strip()
            else:
                self.f2TakedownPercent = "None"

    except Exception as ex:
        print("exception --- error in set takedown percent => {0}".format(ex))
        self.f1TakedownPercent = "None"
        self.f2TakedownPercent = "None"

def setSubmissionAttempt(self,response):
    try:
        # /html/body/section/div/div/section[2]/table/tbody/tr/td[8]/p[1]
        submissionAtt = checkEmpty(response.xpath( \
            "..//html/body/section/div/div/section[2]/table/tbody/tr/td[8]/p/text()").extract())
        if (submissionAtt != "None"):
            self.f1SubmissionAtt = submissionAtt[0].strip()
            self.f2SubmissionAtt = submissionAtt[1].strip()
        else:
            self.f1SubmissionAtt = "None"
            self.f2SubmissionAtt = "None"

    except Exception as ex:
        print("exception --- error in set submission attempt => {0}".format(ex))
        self.f1SubmissionAtt = "None"
        self.f2SubmissionAtt = "None"

def setRev(self,response):
    try:
        # /html/body/section/div/div/section[2]/table/tbody/tr/td[9]/p[1]
        rev = checkEmpty(response.xpath( \
            "..//html/body/section/div/div/section[2]/table/tbody/tr/td[9]/p/text()").extract())
        if (rev != "None"):
            self.f1Rev = rev[0].strip()
            self.f2Rev = rev[1].strip()
        else:
            self.f1Rev = "None"
            self.f2Rev = "None"

    except Exception as ex:
        print("exception --- error in set rev => {0}".format(ex))
        self.f1Rev = "None"
        self.f2Rev = "None"

def setTimeControl(self,response):
    try:
        # /html/body/section/div/div/section[2]/table/tbody/tr/td[10]/p[1]
        timeControl = checkEmpty(response.xpath( \
            "..//html/body/section/div/div/section[2]/table/tbody/tr/td[10]/p/text()").extract())
        if (timeControl != "None" and timeControl != "---"):
            f1MinTimeControl = timeControl[0].split(":")[0].strip()
            f1SecTimeControl = timeControl[0].split(":")[1].strip()
            if (f1MinTimeControl != "0"):
                convF1TimeControl = int(f1MinTimeControl) * 60
                self.f1TimeControl = str(convF1TimeControl + int(f1SecTimeControl))
            else:
                self.f1TimeControl = str(f1SecTimeControl)

            f2MinTimeControl = timeControl[1].split(":")[0].strip()
            f2SecTimeControl = timeControl[1].split(":")[1].strip()
            if (f2MinTimeControl != "0"):
                convF2TimeControl = int(f2MinTimeControl) * 60
                self.f2TimeControl = str(convF2TimeControl + int(f2SecTimeControl))
            else:
                self.f2TimeControl = str(f2SecTimeControl)
        else:
            self.f1TimeControl = "None"
            self.f2TimeControl = "None"

    except Exception as ex:
        print("exception --- error in set time control => {0}".format(ex))
        self.f1TimeControl = "None"
        self.f2TimeControl = "None"

def setSigStrikes(self,response):
    try:
        # /html/body/section/div/div/table/tbody/tr/td[2]/p[1]
        sigStrikes = checkEmpty(response.xpath( \
            "..//html/body/section/div/div/table/tbody/tr/td[2]/p/text()").extract())
        if (sigStrikes != "None"):
            f1SigStrikes = sigStrikes[0].strip()
            f2SigStrikes = sigStrikes[1].strip()

            self.f1SigStrikesLanded = f1SigStrikes.split("of")[0].strip()
            self.f1SigStrikesAtt = f1SigStrikes.split("of")[1].strip()
            self.f2SigStrikesLanded = f2SigStrikes.split("of")[0].strip()
            self.f2SigStrikesAtt = f2SigStrikes.split("of")[1].strip()
        else:
            self.f1SigStrikesLanded = "None"
            self.f1SigStrikesAtt = "None"
            self.f2SigStrikesLanded = "None"
            self.f2SigStrikesAtt = "None"

    except Exception as ex:
        print("exception --- error in set significant strikes => {0}".format(ex))
        self.f1SigStrikesLanded = "None"
        self.f2SigStrikesLanded = "None"
        self.f1SigStrikesAtt = "None"
        self.f2SigStrikesAtt = "None"

def setSigStrikesPercent(self,response):
    try:
        # /html/body/section/div/div/table/tbody/tr/td[3]/p[1]
        sigStrikesPercent = checkEmpty(response.xpath( \
            "..//html/body/section/div/div/table/tbody/tr/td[3]/p/text()").extract())
        if (sigStrikesPercent != "None"):
            self.f1SigStrikesPercent = sigStrikesPercent[0].strip()
            self.f2SigStrikesPercent = sigStrikesPercent[1].strip()

        else:
            self.f1SigStrikesPercent = "None"
            self.f2SigStrikesPercent = "None"

    except Exception as ex:
        print("exception --- error in set significant strikes percent => {0}".format(ex))
        self.f1SigStrikesPercent = "None"
        self.f2SigStrikesPercent = "None"

def setHeadSigStrikes(self,response):
    try:
        # /html/body/section/div/div/table/tbody/tr/td[4]/p[1]
        headSigStrikes = checkEmpty(response.xpath( \
            "..//html/body/section/div/div/table/tbody/tr/td[4]/p/text()").extract())
        if (headSigStrikes != "None"):
            f1HeadSigStrikes = headSigStrikes[0].strip()
            f2HeadSigStrikes = headSigStrikes[1].strip()

            self.f1HeadSigStrikesLanded = f1HeadSigStrikes.split("of")[0].strip()
            self.f1HeadSigStrikesAtt = f1HeadSigStrikes.split("of")[1].strip()
            self.f2HeadSigStrikesLanded = f2HeadSigStrikes.split("of")[0].strip()
            self.f2HeadSigStrikesAtt = f2HeadSigStrikes.split("of")[1].strip()
        else:
            self.f1HeadSigStrikesLanded = "None"
            self.f1HeadSigStrikesAtt = "None"
            self.f2HeadSigStrikesLanded = "None"
            self.f2HeadSigStrikesAtt = "None"

    except Exception as ex:
        print("exception --- error in set head significant strikes => {0}".format(ex))
        self.f1HeadSigStrikesLanded = "None"
        self.f1HeadSigStrikesAtt = "None"
        self.f2HeadSigStrikesLanded = "None"
        self.f2HeadSigStrikesAtt = "None"

def setBodySigStrikes(self,response):
    try:
        # /html/body/section/div/div/table/tbody/tr/td[5]/p[1]
        bodySigStrikes = checkEmpty(response.xpath( \
            "..//html/body/section/div/div/table/tbody/tr/td[5]/p/text()").extract())
        if (bodySigStrikes != "None"):
            f1BodySigStrikes = bodySigStrikes[0].strip()
            f2BodySigStrikes = bodySigStrikes[1].strip()

            self.f1BodySigStrikesLanded = f1BodySigStrikes.split("of")[0].strip()
            self.f1BodySigStrikesAtt = f1BodySigStrikes.split("of")[1].strip()
            self.f2BodySigStrikesLanded = f2BodySigStrikes.split("of")[0].strip()
            self.f2BodySigStrikesAtt = f2BodySigStrikes.split("of")[1].strip()
        else:
            self.f1BodySigStrikesLanded = "None"
            self.f1BodySigStrikesAtt = "None"
            self.f2BodySigStrikesLanded = "None"
            self.f2BodySigStrikesAtt = "None"

    except Exception as ex:
        print("exception --- error in set body significant strikes => {0}".format(ex))
        self.f1BodySigStrikesLanded = "None"
        self.f1BodySigStrikesAtt = "None"
        self.f2BodySigStrikesLanded = "None"
        self.f2BodySigStrikesAtt = "None"

def setLegSigStrikes(self,response):
    try:
        # /html/body/section/div/div/table/tbody/tr/td[6]/p[1]
        legSigStrikes = checkEmpty(response.xpath( \
            "..//html/body/section/div/div/table/tbody/tr/td[6]/p/text()").extract())
        if (legSigStrikes != "None"):
            f1LegSigStrikes = legSigStrikes[0].strip()
            f2LegSigStrikes = legSigStrikes[1].strip()

            self.f1LegSigStrikesLanded = f1LegSigStrikes.split("of")[0].strip()
            self.f1LegSigStrikesAtt = f1LegSigStrikes.split("of")[1].strip()
            self.f2LegSigStrikesLanded = f2LegSigStrikes.split("of")[0].strip()
            self.f2LegSigStrikesAtt = f2LegSigStrikes.split("of")[1].strip()
        else:
            self.f1LegSigStrikesLanded = "None"
            self.f1LegSigStrikesAtt = "None"
            self.f2LegSigStrikesLanded = "None"
            self.f2LegSigStrikesAtt = "None"

    except Exception as ex:
        print("exception --- error in set leg significant strikes => {0}".format(ex))
        self.f1LegSigStrikesLanded = "None"
        self.f1LegSigStrikesAtt = "None"
        self.f2LegSigStrikesLanded = "None"
        self.f2LegSigStrikesAtt = "None"

def setDistanceSigStrikes(self,response):
    try:
        # /html/body/section/div/div/table/tbody/tr/td[7]/p[1]
        distanceSigStrikes = checkEmpty(response.xpath( \
            "..//html/body/section/div/div/table/tbody/tr/td[7]/p/text()").extract())
        if (distanceSigStrikes != "None"):
            f1DistanceSigStrikes = distanceSigStrikes[0].strip()
            f2DistanceSigStrikes = distanceSigStrikes[1].strip()

            self.f1DistanceSigStrikesLanded = f1DistanceSigStrikes.split("of")[0].strip()
            self.f1DistanceSigStrikesAtt = f1DistanceSigStrikes.split("of")[1].strip()
            self.f2DistanceSigStrikesLanded = f2DistanceSigStrikes.split("of")[0].strip()
            self.f2DistanceSigStrikesAtt = f2DistanceSigStrikes.split("of")[1].strip()
        else:
            self.f1DistanceSigStrikesLanded = "None"
            self.f1DistanceSigStrikesAtt = "None"
            self.f2DistanceSigStrikesLanded = "None"
            self.f2DistanceSigStrikesAtt = "None"

    except Exception as ex:
        print("exception --- error in set distance significant strikes => {0}".format(ex))
        self.f1DistanceSigStrikesLanded = "None"
        self.f1DistanceSigStrikesAtt = "None"
        self.f2DistanceSigStrikesLanded = "None"
        self.f2DistanceSigStrikesAtt = "None"

def setClinchSigStrikes(self,response):
    try:
        # /html/body/section/div/div/table/tbody/tr/td[8]/p[1]
        clinchSigStrikes = checkEmpty(response.xpath( \
            "..//html/body/section/div/div/table/tbody/tr/td[8]/p/text()").extract())
        if (clinchSigStrikes != "None"):
            f1ClinchSigStrikes = clinchSigStrikes[0].strip()
            f2ClinchSigStrikes = clinchSigStrikes[1].strip()

            self.f1ClinchSigStrikesLanded = f1ClinchSigStrikes.split("of")[0].strip()
            self.f1ClinchSigStrikesAtt = f1ClinchSigStrikes.split("of")[1].strip()
            self.f2ClinchSigStrikesLanded = f2ClinchSigStrikes.split("of")[0].strip()
            self.f2ClinchSigStrikesAtt = f2ClinchSigStrikes.split("of")[1].strip()
        else:
            self.f1ClinchSigStrikesLanded = "None"
            self.f1ClinchSigStrikesAtt = "None"
            self.f2ClinchSigStrikesLanded = "None"
            self.f2ClinchSigStrikesAtt = "None"

    except Exception as ex:
        print("exception --- error in set clinch significant strikes => {0}".format(ex))
        self.f1ClinchSigStrikesLanded = "None"
        self.f1ClinchSigStrikesAtt = "None"
        self.f2ClinchSigStrikesLanded = "None"
        self.f2ClinchSigStrikesAtt = "None"

def setGroundSigStrikes(self,response):
    try:
        # /html/body/section/div/div/table/tbody/tr/td[9]/p[1]
        groundSigStrikes = checkEmpty(response.xpath( \
            "..//html/body/section/div/div/table/tbody/tr/td[9]/p/text()").extract())
        if (groundSigStrikes != "None"):
            f1GroundSigStrikes = groundSigStrikes[0].strip()
            f2GroundSigStrikes = groundSigStrikes[1].strip()

            self.f1GroundSigStrikesLanded = f1GroundSigStrikes.split("of")[0].strip()
            self.f1GroundSigStrikesAtt = f1GroundSigStrikes.split("of")[1].strip()
            self.f2GroundSigStrikesLanded = f2GroundSigStrikes.split("of")[0].strip()
            self.f2GroundSigStrikesAtt = f2GroundSigStrikes.split("of")[1].strip()
        else:
            self.f1GroundSigStrikesLanded = "None"
            self.f1GroundSigStrikesAtt = "None"
            self.f2GroundSigStrikesLanded = "None"
            self.f2GroundSigStrikesAtt = "None"

    except Exception as ex:
        print("exception --- error in set ground significant strikes => {0}".format(ex))
        self.f1GroundSigStrikesLanded = "None"
        self.f1GroundSigStrikesAtt = "None"
        self.f2GroundSigStrikesLanded = "None"
        self.f2GroundSigStrikesAtt = "None"


# ----------------------------------------------------------------------------------------------------------------------
def setSignificantStrikesTable(self):
    try:
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

    except Exception as ex:
        print("exception --- error in set significant strikes table => {0}".format(ex))

# ----------------------------------------------------------------------------------------------------------------------
def setUrlEvent(self,trTags):
    try:
        # /html/body/section/div/div/div/div[2]/div/table/tbody/tr[3]/td[1]/i/a
        urlEvent = checkEmpty(trTags[1].xpath("..//td[1]/i/a/@href").extract())
        if (urlEvent != "None"):
            self.urlEventList = urlEvent
        else:
            self.urlEventList = "None"

    except Exception as ex:
        print("exception --- error in set url event => {0}".format(ex))
        self.urlEventList = "None"

def setLocationEvent(self,trTags):
    try:
        # /html/body/section/div/div/div/div[2]/div/table/tbody/tr[3]/td[2]
        locationEvent = checkEmpty(trTags[1].xpath("..//td[2]/text()").extract())
        self.locationEventList = locationEvent if (locationEvent != "None") else "None"

    except Exception as ex:
        print("exception --- error in set location event => {0}".format(ex))
        self.locationEventList = "None"

def setDateEvent(self,trTags):
    try:
        # /html/body/section/div/div/div/div[2]/div/table/tbody/tr[3]/td[1]/i/span
        dateEvent = checkEmpty(trTags[1].xpath("..//td[1]/i/span/text()").extract())
        if (dateEvent != "None"):
            self.dateEventList = dateEvent
        else:
            self.dateEventList = "None"

    except Exception as ex:
        print("exception --- error in set date event => {0}".format(ex))
        self.dateEventList = "None"

# ----------------------------------------------------------------------------------------------------------------------
def setDateEventDetails(self,**kwargs):
    try:
        self.dateEventDetails = kwargs["date"].strip()

    except Exception as ex:
        print("exception --- error in set date event details => {0}".format(ex))
        self.dateEventDetails = "None"

def setDateUpcomingDetails(self,**kwargs):
    try:
        self.dateUpcomingDetails = kwargs["date"].strip()

    except Exception as ex:
        print("exception --- error in set date upcoming details => {0}".format(ex))
        self.dateUpcomingDetails = "None"

def setLocationEventDetails(self,**kwargs):
    try:
        self.locationEventDetails = kwargs["location"].strip()

    except Exception as ex:
        print("exception --- error in set location event details => {0}".format(ex))
        self.locationEventDetails = "None"

def setLocationUpcomingDetails(self,**kwargs):
    try:
        locationUpcomingDetails = kwargs["location"].strip()
        self.locationUpcomingDetails = locationUpcomingDetails if (locationUpcomingDetails != "---" and locationUpcomingDetails != "None") else "None"

    except Exception as ex:
        print("exception --- error in set location upcoming details => {0}".format(ex))
        self.locationUpcomingDetails = "None"

# ----------------------------------------------------------------------------------------------------------------------
def setEventNameUpcoming(self,response):
    try:
        # /html/body/section/div/h2/span
        eventName = checkEmpty(response.xpath("..//html/body/section/div/h2/span/text()").get())
        if (eventName != "None"):
            self.eventNameUpcoming = eventName.strip()
        else:
            self.eventNameUpcoming = "None"

    except Exception as ex:
        print("exception --- error in set event name upcoming => {0}".format(ex))
        self.eventNameUpcoming = "None"

def setFighterNameEvent(self,trTags,i):
    try:
        # /html/body/section/div/div/table/tbody/tr[1]/td[2]/p[1]/a
        f1Name = checkEmpty(trTags[i].xpath(".//td[2]/p[1]/a/text()").get())
        f2Name = checkEmpty(trTags[i].xpath(".//td[2]/p[2]/a/text()").get())
        if (f1Name != "None"):
            self.f1Name = f1Name.strip()
        else:
            self.f1Name = "None"

        if (f2Name != "None"):
            self.f2Name = f2Name.strip()
        else:
            self.f2Name = "None"

    except Exception as ex:
        print("exception --- error in set fighter name event => {0}".format(ex))
        self.f1Name = "None"
        self.f2Name = "None"

def setFighterResultEvent(self):
    try:
        if (self.f1Name != "None" and self.f2Name != "None"):
            self.f1Result = "win"
            self.f1ResultEncode = "1"
            self.f2Result = "loss"
            self.f2ResultEncode = "0"
        else:
            self.f1Result = "None"
            self.f1ResultEncode = "None"
            self.f2Result = "None"
            self.f2ResultEncode = "None"

    except Exception as ex:
        print("exception --- error in set fighter result event => {0}".format(ex))
        self.f1Result = "None"
        self.f1ResultEncode = "None"
        self.f2Result = "None"
        self.f2ResultEncode = "None"

def setKnockdownEvent(self,trTags,i):
    try:
        # /html/body/section/div/div/table/tbody/tr[1]/td[3]/p[1]
        f1Knockdown = checkEmpty(trTags[i].xpath(".//td[3]/p[1]/text()").get())
        f2Knockdown = checkEmpty(trTags[i].xpath(".//td[3]/p[2]/text()").get())
        if (f1Knockdown != "None"):
            self.f1Knockdown = f1Knockdown.strip()
        else:
            self.f1Knockdown = "None"

        if (f2Knockdown != "None"):
            self.f2Knockdown = f2Knockdown.strip()
        else:
            self.f2Knockdown = "None"

    except Exception as ex:
        print("exception --- error in set knockdown event => {0}".format(ex))
        self.f1Knockdown = "None"
        self.f2Knockdown = "None"

def setStrikesEvent(self,trTags,i):
    try:
        # /html/body/section/div/div/table/tbody/tr[1]/td[4]/p[1]
        f1Strikes = checkEmpty(trTags[i].xpath(".//td[4]/p[1]/text()").get())
        f2Strikes = checkEmpty(trTags[i].xpath(".//td[4]/p[2]/text()").get())
        if (f1Strikes != "None"):
            self.f1Strikes = f1Strikes.strip()
        else:
            self.f1Strikes = "None"

        if (f2Strikes != "None"):
            self.f2Strikes = f2Strikes.strip()
        else:
            self.f2Strikes = "None"

    except Exception as ex:
        print("exception --- error in set strikes event => {0}".format(ex))
        self.f1Strikes = "None"
        self.f2Strikes = "None"

def setTakedownEvent(self,trTags,i):
    try:
        # /html/body/section/div/div/table/tbody/tr[1]/td[5]/p[1]
        f1Takedown = checkEmpty(trTags[i].xpath(".//td[5]/p[1]/text()").get())
        f2Takedown = checkEmpty(trTags[i].xpath(".//td[5]/p[2]/text()").get())
        if (f1Takedown != "None"):
            self.f1Takedown = f1Takedown.strip()
        else:
            self.f1Takedown = "None"

        if (f2Takedown != "None"):
            self.f2Takedown = f2Takedown.strip()
        else:
            self.f2Takedown = "None"

    except Exception as ex:
        print("exception --- error in set takedown event => {0}".format(ex))
        self.f1Takedown = "None"
        self.f2Takedown = "None"

def setSubmissionEvent(self,trTags,i):
    try:
        # /html/body/section/div/div/table/tbody/tr[1]/td[6]/p[1]
        f1Submission = checkEmpty(trTags[i].xpath(".//td[6]/p[1]/text()").get())
        f2Submission = checkEmpty(trTags[i].xpath(".//td[6]/p[2]/text()").get())
        if (f1Submission != "None"):
            self.f1Submission = f1Submission.strip()
        else:
            self.f1Submission = "None"

        if (f2Submission != "None"):
            self.f2Submission = f2Submission.strip()
        else:
            self.f2Submission = "None"

    except Exception as ex:
        print("exception --- error in set submission event => {0}".format(ex))
        self.f1Submission = "None"
        self.f2Submission = "None"

def setWeightClassEvent(self,trTags,i):
    try:
        # /html/body/section/div/div/table/tbody/tr[1]/td[7]/p
        weightClass = checkEmpty(trTags[i].xpath(".//td[7]/p/text()").get())
        if (weightClass != "None"):
            self.weightClass = weightClass.strip()
        else:
            self.weightClass = "None"

    except Exception as ex:
        print("exception --- error in set weight class event => {0}".format(ex))
        self.weightClass = "None"

def setFightDetailsEvent(self,trTags,i):
    try:
        # /html/body/section/div/div/table/tbody/tr[1]/td[8]/p[1]
        fightDetails = checkEmpty(trTags[i].xpath(".//td[8]/p/text()").extract())
        if (fightDetails != "None"):
            self.fightDetails = fightDetails[0].strip() + " " + fightDetails[1].strip()
        else:
            self.fightDetails = "None"

    except Exception as ex:
        print("exception --- error in set fight details event => {0}".format(ex))
        self.fightDetails = "None"

def setFightLastRoundEvent(self,trTags,i):
    try:
        # /html/body/section/div/div/table/tbody/tr[1]/td[9]/p
        fightLastRound = checkEmpty(trTags[i].xpath(".//td[9]/p/text()").get())
        if (fightLastRound != "None"):
            self.fightLastRound = fightLastRound.strip()
        else:
            self.fightLastRound = "None"

    except Exception as ex:
        print("exception --- error in set fight last round event => {0}".format(ex))
        self.fightLastRound = "None"

def setFightTimeEvent(self,trTags,i):
    try:
        # /html/body/section/div/div/table/tbody/tr[1]/td[10]/p
        fightTime = checkEmpty(trTags[i].xpath(".//td[10]/p/text()").get())
        if (fightTime != "None"):
            self.fightTime = fightTime.strip()
        else:
            self.fightTime = "None"

    except Exception as ex:
        print("exception --- error in set fight time event => {0}".format(ex))
        self.fightTime = "None"








# ----------------------------------------------------------------------------------------------------------------------
def getTime():
    try:
        now = datetime.now()
        currentDate = now.strftime("%m_%d_%y")
        return currentDate

    except Exception as ex:
        print("exception --- error in get time => {0}".format(ex))
        return "None"

def printTime():
    now = datetime.now()
    currentDate = now.strftime("%m_%d_%y")
    return currentDate

def resetFighterStats(self):
    self.birthDate = ""
    self.age = ""
    self.height = ""
    self.weight = ""
    self.win = ""
    self.loss = ""
    self.locality = ""
    self.country = ""

def setLocation(self,location):
    subComma = re.sub(r"[\,]",";",location)
    self.location = '"' + subComma + '"'

def setLocality(self,locality):
    if (re.search(r"N/A",locality) != None):
        self.locality = "None"
    else:
        subComma = re.sub(r"[\,]",";",locality)
        self.locality = '"' + subComma + '"'

def setCountry(self,country):
    if (re.search(r"N/A",country) != None):
        self.country = "None"
    else:
        self.country = country

def setHeight(self,height):
    if (re.search(r"N/A",height) == None and re.search(r"0'0",height) == None):
        subDoubleQuote = re.sub(r"[\"]","",height)
        splitSingleQuote = subDoubleQuote.split("'")
        self.height = str((int(splitSingleQuote[0]) * 12) + int(splitSingleQuote[1]))
    else:
        self.height = "None"

def setWeight(self,weight):
    subLetters = re.sub(r"[^0-9]","",weight)
    if (subLetters != "0"):
        self.weight = subLetters
    else:
        self.weight = "None"

def setAge(self,age):
    subStr = ""
    if (re.search(r"N/A",age) != None):
        self.age = "None"
    else:
        subStr = re.sub(r"AGE:","",age)
        self.age = subStr.strip()

def setBirthDate(self,birthDate):
    month = ""
    day = ""
    year = ""
    if (re.search(r"N/A",birthDate) != None):
        self.birthDate = "None"
    else:
        splitDash = birthDate.split("-")
        month = splitDash[1]
        day  = splitDash[2]
        year = splitDash[0]

        self.birthDate = month + "/" + day + "/" + year

def setAssociation(self,association):
    self.association = str(association).lower()

def setFirstRowFightCard(self,response):
    try:
        f1Name = checkEmpty(response.xpath("//div[@class='fighter left_side']/h3/a/span/text()").get())
        if (f1Name != "None"):
            self.f1Name = f1Name.lower()
        else:
            self.f1Name = "None"

        f1Result = checkEmpty(response.xpath("//div[@class='fighter left_side']/span[1]/text()").get())
        if (f1Result != "None"):
            self.f1Result = checkFightResult(self,f1Result.lower())
        else:
            self.f1Result = "None"

        f2Name = checkEmpty(response.xpath("//div[@class='fighter right_side']/h3/a/span/text()").get())
        if (f2Name != "None"):
            self.f2Name = f2Name.lower()
        else:
            self.f2Name = "None"

        f2Result = checkEmpty(response.xpath("//div[@class='fighter right_side']/span[1]/text()").get())
        if (f2Result != "None"):
            self.f2Result = checkFightResult(self,f2Result.lower())
        else:
            self.f2Result = "None"

        fighterMethodResult = checkEmpty(response.xpath("//div[@class='footer']/table/tbody/tr/td[2]/text()").get())
        if (fighterMethodResult != "None"):
            self.fighterMethodResult = fighterMethodResult.lower()
        else:
            self.fighterMethodResult

    except Exception as ex:
        print("exception: {0}".format(ex))

def checkFightResult(self,fightResult):
    if (fightResult == "win"):
        return "W"
    elif (fightResult == "loss"):
        return "L"

def loadFightStatsItem(self,response):
    try:
        loader = ItemLoader(item=FightStatsItem(), response=response)
        loader.add_value("date", self.date)
        loader.add_value("location", self.location)
        loader.add_value('fightId', self.fightId)
        loader.add_value('f1Name', self.f1Name)
        loader.add_value('f2Name', self.f2Name)
        loader.add_value('f1Id', self.f1Id)
        loader.add_value('f2Id', self.f2Id)
        loader.add_value("f1Result", self.f1Result)
        loader.add_value("f2Result", self.f2Result)
        loader.add_value("f1ResultEncode", self.f1ResultEncode)
        loader.add_value("f2ResultEncode", self.f2ResultEncode)
        # --------------------------------------------------------------------------------------------------------------
        loader.add_value('weightClass', self.weightClass)
        loader.add_value('decisionMethod', self.decisionMethod)
        loader.add_value('fightLastRound', self.fightLastRound)
        loader.add_value('fightTime', self.fightTime)
        loader.add_value("fightTimeFormat", self.fightTimeFormat)
        loader.add_value("fightDetails", self.fightDetails)
        # --------------------------------------------------------------------------------------------------------------
        loader.add_value('f1Knockdown', self.f1Knockdown)
        loader.add_value('f2Knockdown', self.f2Knockdown)
        loader.add_value('f1SigStrikesLandedTotal', self.f1SigStrikesLandedTotal)
        loader.add_value("f2SigStrikesLandedTotal", self.f2SigStrikesLandedTotal)
        loader.add_value('f1SigStrikesAttTotal', self.f1SigStrikesAttTotal)
        loader.add_value("f2SigStrikesAttTotal", self.f2SigStrikesAttTotal)
        loader.add_value('f1SigStrikesPercentTotal', self.f1SigStrikesPercentTotal)
        loader.add_value("f2SigStrikesPercentTotal", self.f2SigStrikesPercentTotal)
        loader.add_value("f1StrikesLandedTotal",self.f1StrikesLandedTotal)
        loader.add_value("f2StrikesLandedTotal",self.f2StrikesLandedTotal)
        loader.add_value("f1StrikesAttTotal", self.f1StrikesAttTotal)
        loader.add_value("f2StrikesAttTotal", self.f2StrikesAttTotal)
        loader.add_value("f1TakedownLanded", self.f1TakedownLanded)
        loader.add_value("f2TakedownLanded", self.f2TakedownLanded)
        loader.add_value("f1TakedownAtt", self.f1TakedownAtt)
        loader.add_value("f2TakedownAtt", self.f2TakedownAtt)
        loader.add_value("f1TakedownPercent", self.f1TakedownPercent)
        loader.add_value("f2TakedownPercent", self.f2TakedownPercent)
        loader.add_value("f1SubmissionAtt", self.f1SubmissionAtt)
        loader.add_value("f2SubmissionAtt", self.f2SubmissionAtt)
        loader.add_value("f1Rev", self.f1Rev)
        loader.add_value("f2Rev", self.f2Rev)
        loader.add_value("f1TimeControl", self.f1TimeControl)
        loader.add_value("f2TimeControl", self.f2TimeControl)
        loader.add_value("f1SigStrikesLanded", self.f1SigStrikesLanded)
        loader.add_value("f2SigStrikesLanded", self.f2SigStrikesLanded)
        loader.add_value("f1SigStrikesAtt", self.f1SigStrikesAtt)
        loader.add_value("f2SigStrikesAtt", self.f2SigStrikesAtt)
        loader.add_value("f1SigStrikesPercent", self.f1SigStrikesPercent)
        loader.add_value("f2SigStrikesPercent", self.f2SigStrikesPercent)
        loader.add_value("f1HeadSigStrikesLanded", self.f1HeadSigStrikesLanded)
        loader.add_value("f2HeadSigStrikesLanded", self.f2HeadSigStrikesLanded)
        loader.add_value("f1HeadSigStrikesAtt", self.f1HeadSigStrikesAtt)
        loader.add_value("f2HeadSigStrikesAtt", self.f2HeadSigStrikesAtt)
        loader.add_value("f1BodySigStrikesLanded", self.f1BodySigStrikesLanded)
        loader.add_value("f2BodySigStrikesLanded", self.f2BodySigStrikesLanded)
        loader.add_value("f1BodySigStrikesAtt", self.f1BodySigStrikesAtt)
        loader.add_value("f2BodySigStrikesAtt", self.f2BodySigStrikesAtt)
        loader.add_value("f1LegSigStrikesLanded", self.f1LegSigStrikesLanded)
        loader.add_value("f2LegSigStrikesLanded", self.f2LegSigStrikesLanded)
        loader.add_value("f1LegSigStrikesAtt", self.f1LegSigStrikesAtt)
        loader.add_value("f2LegSigStrikesAtt", self.f2LegSigStrikesAtt)
        loader.add_value("f1DistanceSigStrikesLanded", self.f1DistanceSigStrikesLanded)
        loader.add_value("f2DistanceSigStrikesLanded", self.f2DistanceSigStrikesLanded)
        loader.add_value("f1DistanceSigStrikesAtt", self.f1DistanceSigStrikesAtt)
        loader.add_value("f2DistanceSigStrikesAtt", self.f2DistanceSigStrikesAtt)
        loader.add_value("f1ClinchSigStrikesLanded", self.f1ClinchSigStrikesLanded)
        loader.add_value("f2ClinchSigStrikesLanded", self.f2ClinchSigStrikesLanded)
        loader.add_value("f1ClinchSigStrikesAtt", self.f1ClinchSigStrikesAtt)
        loader.add_value("f2ClinchSigStrikesAtt", self.f2ClinchSigStrikesAtt)
        loader.add_value("f1GroundSigStrikesLanded", self.f1GroundSigStrikesLanded)
        loader.add_value("f2GroundSigStrikesLanded", self.f2GroundSigStrikesLanded)
        loader.add_value("f1GroundSigStrikesAtt", self.f1GroundSigStrikesAtt)
        loader.add_value("f2GroundSigStrikesAtt", self.f2GroundSigStrikesAtt)
        return loader

    except Exception as ex:
        print("exception --- error in load fight stats item => {0}".format(ex))

def loadEventItem(self,response,i):
    try:
        self.urlEventList[i] = self.urlEventList[i] if (self.urlEventList[i] != "") else "None"
        self.locationEventList[i] = self.locationEventList[i] if (self.locationEventList[i] != "") else "None"
        self.dateEventList[i] = self.dateEventList[i] if (self.dateEventList[i] != "") else "None"

        loader = ItemLoader(item=EventItem(),response=response)
        loader.add_value("urlEvent",self.urlEventList[i].strip())
        loader.add_value("locationEvent", self.locationEventList[i].strip())
        loader.add_value("dateEvent", self.dateEventList[i].strip())
        return loader

    except Exception as ex:
        print("exception --- error in load event item => {0}".format(ex))

def loadUpcomingItem(self,response,i):
    try:
        self.urlEventList[i] = self.urlEventList[i] if (self.urlEventList[i] != "") else "None"
        self.locationEventList[i] = self.locationEventList[i] if (self.locationEventList[i].strip() != "---" and self.locationEventList[i] != "None") else "None"
        self.dateEventList[i] = self.dateEventList[i] if (self.dateEventList[i] != "") else "None"

        loader = ItemLoader(item=UpcomingItem(),response=response)
        loader.add_value("urlEvent",self.urlEventList[i].strip())
        loader.add_value("locationEvent",self.locationEventList[i].strip())
        loader.add_value("dateEvent",self.dateEventList[i].strip())
        return loader

    except Exception as ex:
        print("exception --- error in load upcoming item => {0}".format(ex))

def loadEventDetailsItem(self,response):
    try:
        loader = ItemLoader(item=EventDetailsItem(),response=response)
        loader.add_value("f1Name",self.f1Name)
        loader.add_value("f2Name",self.f2Name)
        loader.add_value("f1Result",self.f1Result)
        loader.add_value("f2Result",self.f2Result)
        loader.add_value("f1ResultEncode", self.f1ResultEncode)
        loader.add_value("f2ResultEncode", self.f2ResultEncode)
        loader.add_value("f1Knockdown",self.f1Knockdown)
        loader.add_value("f2Knockdown",self.f2Knockdown)
        loader.add_value("f1Strikes",self.f1Strikes)
        loader.add_value("f2Strikes",self.f2Strikes)
        loader.add_value("f1Takedown",self.f1Takedown)
        loader.add_value("f2Takedown",self.f2Takedown)
        loader.add_value("f1Submission",self.f1Submission)
        loader.add_value("f2Submission",self.f2Submission)
        loader.add_value("weightClass",self.weightClass)
        loader.add_value("fightDetails",self.fightDetails)
        loader.add_value("fightLastRound",self.fightLastRound)
        loader.add_value("fightTime",self.fightTime)
        loader.add_value("dateEventDetails",self.dateEventDetails)
        loader.add_value("locationEventDetails",self.locationEventDetails)
        return loader

    except Exception as ex:
        print("exception --- error in load event details item => {0}".format(ex))

def loadUpcomingDetailsItem(self,response):
    try:
        loader = ItemLoader(item=UpcomingDetailsItem(),response=response)
        loader.add_value("eventNameUpcoming",self.eventNameUpcoming)
        loader.add_value("dateUpcomingDetails", self.dateUpcomingDetails)
        loader.add_value("locationUpcomingDetails", self.locationUpcomingDetails)
        loader.add_value("f1Name",self.f1Name)
        loader.add_value("f2Name",self.f2Name)
        loader.add_value("weightClass",self.weightClass)
        return loader

    except Exception as ex:
        print("exception --- error in load upcoming details item => {0}".format(ex))

def resetFightCard(self):
    self.fighter1Name = ""
    self.fighter2Name = ""
    self.fighter1Result = ""
    self.fighter2Result = ""
    self.fighterMethodResult = ""

def checkHeight(data):
    subDoubleQuote = re.sub(r"[\"\\]",'',data)
    if (subDoubleQuote == "0'0" or subDoubleQuote == None):
        subDoubleQuote = "None"
        return subDoubleQuote
    else:
        splitSingleQuote = subDoubleQuote.split("'")
        convInches = (int(splitSingleQuote[0])) * 12 + int(splitSingleQuote[1])
        return str(convInches)

def checkEmpty(data):
    try:
        if (len(data) == 0):
            data = "None"
            return data
        else:
            return data

    except Exception as ex:
        print("exception --- error in check empty => {0}".format(ex))
