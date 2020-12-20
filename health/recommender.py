class Recommendation():
    DAILY_STANDARD_VALUE = 0

    def __init__(self, input, days):
        self.input = input
        self.days = days

    def get_daily_average(self):
        return int(self.input / self.days)

    def evaluate(self):
        return self.get_daily_average() > self.DAILY_STANDARD_VALUE


class DailyStepsRecommendation(Recommendation):
    DAILY_STANDARD_VALUE = 3000

    def __init__(self, input, days):
        super().__init__(input, days)

    def evaluate(self):
        if super().evaluate() and self.days > 1:
            return f"You averaged {self.get_daily_average()} steps per day, keep up the good walk!"
        elif super().evaluate() and self.days == 1:
            return f"You beat the recommended minimum steps per day of {self.DAILY_STANDARD_VALUE}, keep up the good walk!"

        return f"You didn't make the standard daily steps count of {self.DAILY_STANDARD_VALUE}, step up friend!"


class DailyActivityRecommendation(Recommendation):
    DAILY_STANDARD_VALUE = 60
    tips = "These activities do help promote better physical and mental health."

    def __init__(self, input, days):
        super().__init__(input, days)

    def evaluate(self):
        if super().evaluate() and self.days == 1:
            return f"You recorded {self.input} minutes of healthy activities, good job if you do keep it consistent!"
        elif super().evaluate() and self.days > 1:
            return f"You recorded {self.input} minutes of healthy activities over a period of {self.days} days, averaging {self.get_daily_average} per day. Keep up the good work! {self.tips}"
        else:
            return f"You didn't record up to the standard {self.DAILY_STANDARD_VALUE} minuites of daily healthy activities, hope you pull more minutes next time. {self.tips}"


    # REPORT = ""

    # def __init__(self, steps, days):
    #     self.steps = steps
    #     self.days = days
    #     self.REPORT = f"You made {self.steps} steps in {self.days} days. "

    # def recommend(self):
    #     if (self.steps/self.days) < self.STEPS_PER_DAY:
    #         message = f"The minimum number of steps per day to stay healthy is {self.STANDARD_STEPS_PER_DAY}, you need to walk more."
    #         return self.REPORT + message
    #     else:
    #         message = f"You beat the {self.STANDARD_STEPS_PER_DAY} steps per day mark! Keep up the good walk."
    #         return self.REPORT + message
