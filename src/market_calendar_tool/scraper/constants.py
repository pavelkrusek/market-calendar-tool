from enum import Enum


class Site(Enum):
    FOREXFACTORY = "https://www.forexfactory.com/calendar"
    METALSMINE = "https://www.metalsmine.com/calendar"
    ENERGYEXCH = "https://www.energyexch.com/calendar"
    CRYPTOCRAFT = "https://www.cryptocraft.com/calendar"


site_number_mapping = {
    Site.FOREXFACTORY: 1,
    Site.METALSMINE: 2,
    Site.ENERGYEXCH: 3,
    Site.CRYPTOCRAFT: 4,
}
