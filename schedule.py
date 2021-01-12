
import datetime
import sheets as s
import math

spreadsheet_id = "1ds-26RMErswzXruiUeBruyy2FiHuDdHylNU8z9CgTqs"
range_rotations = "DataRotations"
range_lads = "DataLads"

rotations = {}
lads = {}

daymap = {
    "mo" : 0,
    "tu" : 1,
    "we" : 2,
    "th" : 3,
    "fr" : 4,
    "sa" : 5,
    "su" : 6
}

class Rotation():
    def __init__(self, row):
        self.name = ""
        self.start_week = 0
        self.start_date = datetime.date(1990,1,1)
        self.loop_week = 0
        self.date_hol_start = None
        self.date_hol_end = None
        try:
            self.name = row[0]
            self.start_week = int(row[1])
            self.start_date = datetime.datetime.strptime(row[2], "%d-%m-%y").date()
            self.loop_week = int(row[3])
            self.date_hol_start = datetime.datetime.strptime(row[4], "%d-%m-%y").date()
            self.date_hol_end = datetime.datetime.strptime(row[5], "%d-%m-%y").date()
        except IndexError:
            pass

    def dateInHoliday(self, date):
        if self.date_hol_start == None:
            pass
        elif date < self.date_hol_start:
            return False

        if self.date_hol_end == None:
            pass
        elif date > self.date_hol_end:
            return False

        return True
        
    def __repr__(self):
        return f"Rotation({self.name},{self.start_week},{self.loop_week},{self.date_hol_start},{self.date_hol_end})"

class Lad():
    def __init__(self, row): #sheet	rotation	weekend	available	discord	assume
        self.name = row[0]
        self.range_week = row[1]
        self.rotation = row[2]
        if len(self.rotation) == 0: self.rotation = None
        self.range_weekend = row[3]
        self.available = row[4].split(",")
        try:
            self.discord = int(row[5])
        except ValueError:
            self.discord = None
        self.report = row[6]
        self.updateTimetable()

    def __repr__(self):
        return "Lad(" + self.name + ")"

    def getRotation(self):
        global rotations
        try:
            return rotations[self.rotation]
        except KeyError:
            return None

    def updateTimetable(self):
        global daymap
        rot = self.getRotation()
        self.timetable = {}
        if len(self.range_week) > 0:
            result = s.sheets.values().get(spreadsheetId=spreadsheet_id, range=self.range_week).execute()
            values = result.get("values", [])
            row_weeks = values[0]
            row_days = values[1]
            weeks = []
            days = []

            for x in row_weeks:
                if x.startswith("WEEK "):
                    weeks.append(int(x[5:]))
                else:  
                    weeks.append(None)

            for i in range(len(row_days)):
                st = row_days[i][:2].lower()
                try:
                    n = daymap[st]
                    lastweek = rot.start_week
                    for w in weeks[:i+1]:
                        if type(w) == type(0):
                            lastweek = w
                    days.append(n + (lastweek - rot.start_week) * 7)
                except KeyError:
                    days.append(None)

            for row in values[2:]:
                time = datetime.datetime.strptime(row[0], "%H:%M").time()
                #print(time)
                for dayindex in range(len(days)):
                    day = days[dayindex]

                    if day != None:
                        obj = None
                        try:
                            obj = row[dayindex]
                        except IndexError:
                            obj = ""

                        if len(obj) == 0 or obj in self.available:
                            obj = None
                    
                        if not day in self.timetable:
                            self.timetable[day] = []
                        self.timetable[day].append((time, obj))
            
            for day in self.timetable:
                sorted(self.timetable[day], key=lambda x: x[0])

    def getScheduleDayTime(self, dt):
        rot = self.getRotation()
        if rot == None:
            return None, None
        d = dt.date()
        t = dt.time()
        diff = d - rot.start_date
        wday = None
        if rot.loop_week == 0:
            wday = diff.days
        else:
            ddiv = 7 * rot.loop_week
            ddays = math.floor(diff.days / ddiv) * ddiv
            loop_start = rot.start_date + datetime.timedelta(days = ddays)
            wday = (d - loop_start).days

        return (wday, t)

    def getActivity(self, dt):
        wday, t = self.getScheduleDayTime(dt)
        
        if wday == None:
            return None

        try:
            day = self.timetable[wday]
        except KeyError:
            return None

        if t < day[0][0]:
            return None
        
        current_ac = None
        for slot in day:
            if slot[0] <= t:
                current_ac = slot[1]

        return current_ac

    def getNextActivitySlot(self, dt):
        wday, t = self.getScheduleDayTime(dt)
        
        try:
            day = self.timetable[wday]
        except KeyError:
            return None
        
        current_ac = None
        for slot in day:
            if slot[0] > t:
                if slot[1] != None:
                    current_ac = slot
                    break

        return current_ac

    def getNextFreeSlot(self, dt):
        wday, t = self.getScheduleDayTime(dt)
        
        try:
            day = self.timetable[wday]
        except KeyError:
            return None
        
        current_ac = None
        for slot in day:
            if slot[0] > t:
                if slot[1] == None:
                    current_ac = slot
                    break

        return current_ac

    def getNextFreePeriod(self, dt):
        first = self.getActivity(dt)

        if first != None:
            first = self.getNextFreeSlot(dt)
            if first != None:
                first = first[0]

        second = self.getNextActivitySlot(datetime.datetime.combine(dt.date(), first or dt.time()))
        if second != None:
            second = second[0]

        print(first, second)
        return first, second

    def getNextFreePeriodMessage(self, dt):
        f, s = self.getNextFreePeriod(dt)
        if f == None:
            if s == None:
                return "%NAME %is free for the rest of the day."
            else:
                return "%NAME %is free right now until " + s.strftime("%H:%M") + "."
        else:
            if s == None:
                return "%NAME will be available from " + f.strftime("%H:%M") + " on."
            else:
                return "%NAME %is next available from " + f.strftime("%H:%M") + " to " + s.strftime("%H:%M") + "."

    def getLongFreePeriodMessage(self, dt):
        f, s = self.getNextFreePeriod(dt)
        if f == None:
            if s == None:
                return "%NAME %is free for the rest of the day."
            else:
                return "%NAME %is free right now until " + s.strftime("%H:%M") + "."
        else:
            if s == None:
                return "%NAME will be available from " + f.strftime("%H:%M") + " on."
            else:
                return "%NAME %is next available from " + f.strftime("%H:%M") + " to " + s.strftime("%H:%M") + "."
                    
def updateRotations():
    global rotations
    result = s.sheets.values().get(spreadsheetId=spreadsheet_id, range=range_rotations).execute()
    values = result.get("values", [])
    rotations = {}
    for row in values[1:]:
        print(row)
        if len(row[0]) > 0:
            new = Rotation(row)
            rotations[new.name] = new


def updateLads():
    global lads
    result = s.sheets.values().get(spreadsheetId=spreadsheet_id, range=range_lads).execute()
    values = result.get("values", [])
    lads = {}
    for row in values[1:]:
        new = Lad(row)
        if new.report == "yes":
            lads[new.name] = new

def getPunctuatedListString(l):
    if len(l) == 0:
        return ""
    elif len(l) == 1:
        return l[0]
    else:
        return ", ".join(l[:-1]) + " and " + l[-1]

def getNextFreePeriods(dt):
    lines = {}
    for name in lads:
        lad = lads[name]
        stri = lad.getNextFreePeriodMessage(dt)
        if stri not in lines:
            lines[stri] = []
        lines[stri].append(lad.name)
    out = ""
    for line in lines:
        names = lines[line]
        out += line.replace("%NAME",getPunctuatedListString(names)).replace("%is",len(names) > 1 and "are" or "is") + "\n"
    return out

def getLongFreePeriodsAfter(dt):
    lines = {}
    for name in lads:
        lad = lads[name]
        stri = lad.getNextFreePeriodMessage(dt)
        if stri not in lines:
            lines[stri] = []
        lines[stri].append(lad.name)
    out = ""
    for line in lines:
        names = lines[line]
        out += line.replace("%NAME",getPunctuatedListString(names)).replace("%is",len(names) > 1 and "are" or "is") + "\n"
    return out
    

if __name__ == "__main__":
    s.init()
    updateRotations()
    updateLads()

    