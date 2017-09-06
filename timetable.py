from collections import defaultdict

def hhmm2min(t):
    t = map(int,t.split(':'))
    return t[0] * 60 + t[1]

class TimeTable:
    def __init__(self):
        self.slot_min = 30
        self.begin_hour = 8
        self.end_hour = 22
        self.events = defaultdict( list )
        self.color = { "Lecture" : "#e66101" , "Workshop" : "#fdb863" , "Activity" : "#b2abd2" }

    def addEvent(self, event):
        event['start_min'] = hhmm2min( event['Start'] )
        event['end_min'] = hhmm2min( event['End'] )
        event['unit'] = (event['end_min'] - event['start_min']) / self.slot_min
        assert event['start_min'] <= event['end_min'], event
        self.events[event['Day']].append(event)


    def printHTML(self):
        ret = """<style>table {
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid black;
        }</style>"""

        ret += "<table width='100%' border=1>\n"
        days = sorted(self.events.keys())
        ret += "<thead>\n"
        ret += "\t<th width='{}%'>Time</th>\n".format(100/len(days))

        for d in days:
            ret += "\t<th>Day %s</th>\n" % d

        ret += "</thead>\n"
        ret += "<tbody>\n"

        occupied = defaultdict( set )

        for t in range(self.begin_hour * 60, self.end_hour * 60, self.slot_min):
            hh = "%02d" % (t / 60)
            mm = "%02d" % (t % 60)

            ret += "\t\t<tr>\n"

            if mm == "00":
                ret += "\t\t\t<td rowspan='2'>{}:{}</td>\n".format(hh,mm)

            for d in days:
                
                if t in occupied[d]: continue

                has_event = False
                for event in self.events[d]:
                    if event['start_min'] == t:
                        has_event = True
                        ret += "\t\t\t<td align='center' rowspan='{}' style='background-color:{}'>{}<br/><strong>{}</strong></td>\n".format(
                                event['unit'], self.color[event['Type']], event['Title'], event['Name'])

                        for i in range(event['unit']):
                            occupied[d].add(t+i*self.slot_min)

                if not has_event:
                    ret += "\t\t\t<td>&nbsp</td>\n"


            ret += "\t\t</tr>\n"

        ret += "</tbody>\n"

        ret += "</table>\n"
        return ret 

def main():
    import csv

    timetable = TimeTable()
    with open("example/schedule.csv", "r") as inp:
        reader = csv.DictReader(inp)
        for row in reader:
            timetable.addEvent(row)

    print timetable.printHTML()

if __name__ == "__main__":
    main()
