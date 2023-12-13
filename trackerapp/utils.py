from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import DoseInfo

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):
		events_per_day = events.filter(dose_timing__day=day)
		d = ''
		for event in events_per_day:
			event.dose_timing = event.dose_timing.strftime('%I:%M %p')
			d += f'<li class="text-success fs-6"> {event.dose_timing}</li>'
		
		if day != 0:
			return f"<td><span class='date fw-bold fs-6'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		events = DoseInfo.objects.filter(dose_timing__year=self.year, dose_timing__month=self.month)
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar table table-bordered border-secondary-subtle table-hover table-sm">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		cal += f'</table>'
		return cal