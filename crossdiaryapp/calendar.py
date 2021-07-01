from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import CrossDiary, CrossDiaryContent
from datetime import datetime

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, user_a=None, user_b=None):
        self.year = year
        self.month = month
        self.crossdiary = CrossDiary.objects.get(user_a=user_a, user_b=user_b)
        self.now = datetime.today()
        self.month_name = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'Septempbar', 'October', 'November', 'December']
        self.day_abbr = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
        super(Calendar, self).__init__()

    # 일을 td 태그로 변환하고 이벤트를 일순으로 필터
    def formatday(self, day, weekday):
        feeling_dict = {
            'joy':'happy.png',
            'angry': 'angry.png',
            'sad':'sad.png',
            'fear':'confused.png'
        }
        if (self.year < self.now.year) or (self.year == self.now.year and self.month < self.now.month):
            if day != 0:
                if weekday != 0:
                    try:
                        check = CrossDiaryContent.objects.get(cross=self.crossdiary, date__year=self.year, date__month=self.month, date__day=day)
                        key = check.pk
                        feel = feeling_dict[check.feeling]
                        return f'<a href="../../read/{key}" style="text-decoration: none; color: black;"><li style="border-left: 1px solid #aaaaaa;"><span class="date" style="padding-left: 4px;">{day}</span><br><div style="text-align: center;"><img src="../../../static/{feel}" style="max-width:40px;"></div></li></a>'
                    except:
                        return f'<a href="../../create/{self.year}/{self.month}/{day}/{self.crossdiary.user_a}/{self.crossdiary.user_b}/" style="text-decoration: none; color: black;"><li style="border-left: 1px solid #aaaaaa;"><span class="date" style="padding-left: 4px;">{day}</span></li></a>'
                else:
                    try:
                        check = CrossDiaryContent.objects.get(cross=self.crossdiary, date__year=self.year, date__month=self.month, date__day=day)
                        return f'<a href="../../read/{check.pk}" style="text-decoration: none; color: black;"><li><span class="date" style="padding-left: 4px;">{day}</span><br><div style="text-align: center;"><img src="../../../static/{feeling_dict[check.feeling]}" style="max-width:40px;"></div></li></a>'
                    except:
                        return f'<a href="../../create/{self.year}/{self.month}/{day}/{self.crossdiary.user_a}/{self.crossdiary.user_b}/" style="text-decoration: none; color:black;"><li><span class="date">{day}</span></li></a>'
            else:
                if weekday !=0:
                    return '<li style="border-left: 1px solid #aaaaaa;"></li>'
                else:
                    return '<li></li>'
        elif self.year == self.now.year and self.month == self.now.month:
            if day > self.now.day:
                if day != 0:
                    if weekday != 0:
                        return f'<li style="border-left: 1px solid #aaaaaa; background-color: #FFE6E6;"><span class="date" style="padding-left: 4px;">{day}</span></li>'
                    else:
                        return f'<li style="background-color: #FFE6E6;"><span class="date" style="padding-left: 4px;">{day}</span></li>'
                else:
                    if weekday !=0:
                        return '<li style="border-left: 1px solid #aaaaaa;"></li>'
                    else:
                        return '<li></li>'
            else:
                if day != 0:
                    if weekday != 0:
                        try:
                            check = CrossDiaryContent.objects.get(cross=self.crossdiary, date__year=self.year, date__month=self.month, date__day=day)
                            key = check.pk
                            feel = feeling_dict[check.feeling]
                            return f'<a href="../../read/{key}" style="text-decoration: none; color: black;"><li style="border-left: 1px solid #aaaaaa;"><span class="date" style="padding-left: 4px;">{day}</span><br><div style="text-align: center;"><img src="../../../static/{feel}" style="max-width:40px;"></div></li></a>'
                        except:
                            return f'<a href="../../create/{self.year}/{self.month}/{day}/{self.crossdiary.user_a}/{self.crossdiary.user_b}/" style="text-decoration: none; color: black;"><li style="border-left: 1px solid #aaaaaa;"><span class="date" style="padding-left: 4px;">{day}</span></li></a>'
                    else:
                        try:
                            check = CrossDiaryContent.objects.get(cross=self.crossdiary, date__year=self.year, date__month=self.month, date__day=day)
                            return f'<a href="../../read/{check.pk}" style="text-decoration: none; color: black;"><li><span class="date" style="padding-left: 4px;">{day}</span><br><div style="text-align: center;"><img src="../../../static/{feeling_dict[check.feeling]}" style="max-width:40px;"></div></li></a>'
                        except:
                            return f'<a href="../../create/{self.year}/{self.month}/{day}/{self.crossdiary.user_a}/{self.crossdiary.user_b}/" style="text-decoration: none; color:black;"><li><span class="date">{day}</span></li></a>'
                else:
                    if weekday !=0:
                        return '<li style="border-left: 1px solid #aaaaaa;"></li>'
                    else:
                        return '<li></li>'
        elif self.year == self.now.year and self.month > self.now.month:
            if day != 0:
                if weekday != 0:
                    return f'<li style="border-left: 1px solid #aaaaaa; background-color: #FFE6E6;"><span class="date" style="padding-left: 4px;">{day}</span></li>'
                else:
                    return f'<li style="background-color: #FFE6E6;"><span class="date" style="padding-left: 4px;">{day}</span></li>'
            else:
                if weekday !=0:
                    return '<li style="border-left: 1px solid #aaaaaa;"></li>'
                else:
                    return '<li></li>'
        elif self.year > self.now.year:
            if day != 0:
                if weekday != 0:
                    return f'<li style="border-left: 1px solid #aaaaaa; background-color: #FFE6E6;"><span class="date" style="padding-left: 4px;">{day}</span></li>'
                else:
                    return f'<li style="background-color: #FFE6E6;"><span class="date" style="padding-left: 4px;">{day}</span></li>'
            else:
                if weekday !=0:
                    return '<li style="border-left: 1px solid #aaaaaa;"></li>'
                else:
                    return '<li></li>'

    # 주를 tr 태그로 변환
    def formatweek(self, theweek):
        week = ""
        #print(theweek)
        for d, weekday in theweek:
            week += self.formatday(d, weekday)
        return f'<ul class="calendar_day"> {week} </ul>'

    # 상단 년, 월 표시
    def formatmonthname(self, theyear, themonth, withyear=True):
        m = '%s' % (self.month_name[themonth])
        y = '%s' % (theyear)
        return '<div class="calendar_head"><span style="font-size: 24px; font-family: "Noto Sans", sans-serif;">%s</span>&nbsp&nbsp&nbsp<span style="font-size:24px;">%s</span></div>' % (m, y)

    def formatweekday(self, day):
        """
        Return a weekday name as a table header.
        """
        return '<li class="%s" style="width: 115px;">%s</li>' % (
            self.cssclasses_weekday_head[day], self.day_abbr[day])

    def formatweekheader(self):
        """
        Return a header for a week as a table row.
        """
        s = ''.join(self.formatweekday(i) for i in self.iterweekdays())
        return '<ul class="calendar_weekhead" style="padding-left: 0">%s</ul>' % s

    # 월을 테이블 태그로 변환
    def formatmonth(self, withyear=True):
        cal = f'<div class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week)}\n'
        cal += f'</div>'
        return cal