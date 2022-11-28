# define the models for your scraped items
# see documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
# from scrapy.loader.processors import Identity,TakeFirst,Compose,MapCompose,Join
from itemloaders.processors import Join,MapCompose,TakeFirst,Compose,Identity

STR_toInt = Compose(TakeFirst(),int)
STR_toFloat = Compose(TakeFirst(),float)

def stripPercent(str_input):
    number = str_input.strip('%')
    return float(number) / 100

class FightStatsItem(scrapy.Item):
    fightId = scrapy.Field()
    date = scrapy.Field()
    location = scrapy.Field()
    f1Name = scrapy.Field()
    f2Name = scrapy.Field()
    f1Id = scrapy.Field()
    f2Id = scrapy.Field()
    f1Result = scrapy.Field()
    f2Result = scrapy.Field()
    f1ResultEncode = scrapy.Field()
    f2ResultEncode = scrapy.Field()

    weightClass = scrapy.Field()
    decisionMethod = scrapy.Field()
    fightLastRound = scrapy.Field()
    fightTime = scrapy.Field()
    fightTimeFormat = scrapy.Field()
    fightDetails = scrapy.Field()

    f1Knockdown = scrapy.Field()
    f2Knockdown = scrapy.Field()
    f1SigStrikesLandedTotal = scrapy.Field()
    f2SigStrikesLandedTotal = scrapy.Field()
    f1SigStrikesAttTotal = scrapy.Field()
    f2SigStrikesAttTotal = scrapy.Field()
    f1SigStrikesPercentTotal = scrapy.Field()
    f2SigStrikesPercentTotal = scrapy.Field()
    f1StrikesLandedTotal = scrapy.Field()
    f2StrikesLandedTotal = scrapy.Field()
    f1StrikesAttTotal = scrapy.Field()
    f2StrikesAttTotal = scrapy.Field()
    f1TakedownLanded = scrapy.Field()
    f2TakedownLanded = scrapy.Field()
    f1TakedownAtt = scrapy.Field()
    f2TakedownAtt = scrapy.Field()
    f1TakedownPercent = scrapy.Field()
    f2TakedownPercent = scrapy.Field()
    f1SubmissionAtt = scrapy.Field()
    f2SubmissionAtt = scrapy.Field()
    f1Rev = scrapy.Field()
    f2Rev = scrapy.Field()
    f1TimeControl = scrapy.Field()
    f2TimeControl = scrapy.Field()
    f1SigStrikesLanded = scrapy.Field()
    f2SigStrikesLanded = scrapy.Field()
    f1SigStrikesAtt = scrapy.Field()
    f2SigStrikesAtt = scrapy.Field()
    f1SigStrikesPercent = scrapy.Field()
    f2SigStrikesPercent = scrapy.Field()
    f1HeadSigStrikesLanded = scrapy.Field()
    f2HeadSigStrikesLanded = scrapy.Field()
    f1HeadSigStrikesAtt = scrapy.Field()
    f2HeadSigStrikesAtt = scrapy.Field()
    f1BodySigStrikesLanded = scrapy.Field()
    f2BodySigStrikesLanded = scrapy.Field()
    f1BodySigStrikesAtt = scrapy.Field()
    f2BodySigStrikesAtt = scrapy.Field()
    f1LegSigStrikesLanded = scrapy.Field()
    f2LegSigStrikesLanded = scrapy.Field()
    f1LegSigStrikesAtt = scrapy.Field()
    f2LegSigStrikesAtt = scrapy.Field()
    f1DistanceSigStrikesLanded = scrapy.Field()
    f2DistanceSigStrikesLanded = scrapy.Field()
    f1DistanceSigStrikesAtt = scrapy.Field()
    f2DistanceSigStrikesAtt = scrapy.Field()
    f2ClinchSigStrikesAtt = scrapy.Field()
    f1ClinchSigStrikesLanded = scrapy.Field()
    f2ClinchSigStrikesLanded = scrapy.Field()
    f1ClinchSigStrikesAtt = scrapy.Field()
    f2ClinchSigStrikesAtt = scrapy.Field()
    f1GroundSigStrikesLanded = scrapy.Field()
    f2GroundSigStrikesLanded = scrapy.Field()
    f1GroundSigStrikesAtt = scrapy.Field()
    f2GroundSigStrikesAtt = scrapy.Field()

class EventItem(scrapy.Item):
    try:
        urlEvent = scrapy.Field()
        locationEvent = scrapy.Field()
        dateEvent = scrapy.Field()

    except Exception as ex:
        print("exception --- error in class event item => {0}".format(ex))

class UpcomingItem(scrapy.Item):
    try:
        urlEvent = scrapy.Field()
        locationEvent = scrapy.Field()
        dateEvent = scrapy.Field()

    except Exception as ex:
        print("exception --- error in class upcoming item => {0}".format(ex))

class EventDetailsItem(scrapy.Item):
    try:
        f1Name = scrapy.Field()
        f2Name = scrapy.Field()
        f1Result = scrapy.Field()
        f2Result = scrapy.Field()
        f1ResultEncode = scrapy.Field()
        f2ResultEncode = scrapy.Field()
        f1Knockdown = scrapy.Field()
        f2Knockdown = scrapy.Field()
        f1Strikes = scrapy.Field()
        f2Strikes = scrapy.Field()
        f1Takedown = scrapy.Field()
        f2Takedown = scrapy.Field()
        f1Submission = scrapy.Field()
        f2Submission = scrapy.Field()
        weightClass = scrapy.Field()
        fightDetails = scrapy.Field()
        fightLastRound = scrapy.Field()
        fightTime = scrapy.Field()
        dateEventDetails = scrapy.Field()
        locationEventDetails = scrapy.Field()

    except Exception as ex:
        print("exception --- error in class event details item => {0}".format(ex))

class UpcomingDetailsItem(scrapy.Item):
    try:
        eventNameUpcoming = scrapy.Field()
        dateUpcomingDetails = scrapy.Field()
        locationUpcomingDetails = scrapy.Field()
        f1Name = scrapy.Field()
        f2Name = scrapy.Field()
        weightClass = scrapy.Field()

    except Exception as ex:
        print("exception --- error in class upcoming details item => {0}".format(ex))

class FightSummaryItem(scrapy.Item):
    # define fields for item
    fighter_id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    height = scrapy.Field(output_processor=TakeFirst())
    weight = scrapy.Field(output_processor=TakeFirst())
    reach = scrapy.Field(output_processor=TakeFirst())
    stance = scrapy.Field(output_processor=TakeFirst())
    date_of_birth = scrapy.Field(output_processor=TakeFirst())
    n_win = scrapy.Field(output_processor=STR_toInt)
    n_loss = scrapy.Field(output_processor=STR_toInt)
    n_draw = scrapy.Field(output_processor=STR_toInt)
    signif_strikes_landed_per_minute = scrapy.Field(output_processor=STR_toFloat)
    signif_striking_accuracy = scrapy.Field(output_processor=Compose(TakeFirst(),stripPercent))
    signif_strikes_absorbed_per_minute = scrapy.Field(output_processor=STR_toFloat)
    signif_strikes_defense = scrapy.Field(output_processor=Compose(TakeFirst(), stripPercent))
    takedown_average = scrapy.Field(output_processor=STR_toFloat)
    takedown_accuracy = scrapy.Field(output_processor=Compose(TakeFirst(),stripPercent))
    takedown_defense = scrapy.Field(output_processor=Compose(TakeFirst(),stripPercent))
    submission_average = scrapy.Field(output_processor=STR_toFloat)
