from otree.api import *
import itertools
import random

doc = """
Study 2: the blaming mechanism
"""


# FUNCTION
def creating_session(subsession):
    treatment_cycle = itertools.cycle(['baseline', 'blame', 'nonblame'])
    for player in subsession.get_players():
        player.treatment = next(treatment_cycle)


def likert1(label):
    return models.IntegerField(
        initial=0,
        choices=[[1, ''], [2, ''], [3, ''], [4, ''], [5, '']],
        label=label,
        widget=widgets.RadioSelect)


# PARAMETERS
class C(BaseConstants):
    NAME_IN_URL = 's2pt1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # feedback question
    DEMAND = [
        dict(name='believe', label='I made up my mind in which of the options I believed most and then ticked it.'),
        dict(name='against', label='I made up my mind about which of the options the researchers wanted me to tick '
                                   'and then ticked something else.'),
        dict(name='conform', label='I made up my mind about which of the options the researchers wanted me to tick '
                                   'and then ticked it.'),
        dict(name='random', label='I just made a random guess, like mentally flipping a coin.')
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Exclude bots
    AIuse = models.BooleanField(
        label='If you have used any AI tool in completing this study, please tick "Yes". '
              'You will receive the study reward independent of your answer.'
    )
    answer = models.IntegerField(blank=True)
    aqvideo_attempts = models.IntegerField(initial=0)
    aqvideo = models.BooleanField(initial=0)

    # Treatment assignment
    treatment = models.StringField()

    # Demographics
    age = models.IntegerField(
        label='Age'
    )
    gender = models.StringField(
        widget=widgets.RadioSelect,
        label='Gender',
        choices=['Male', 'Female', 'Non-binary', 'Prefer not to say']
    )
    education = models.StringField(
        widget=widgets.RadioSelect,
        label='Highest education level',
        choices=['No formal education', 'Primary school', 'Secondary school',
                 'University', 'Postgraduate', 'Prefer not to say']
    )
    employ = models.StringField(
        label='What is your current employment status?',
        choices=['Full-time employee', 'Part-time employee', 'Self-employed or small business owner',
                 'Unemployed and looking for work', 'Not currently working and not looking for work',
                 'Student', 'Retiree', 'Prefer not to say']
    )
    region = models.StringField(
        label='Please tell us your region of residence.',
        choices=['North East (England)', 'North West (England)', 'Yorkshire and The Humber (England)',
                 'East Midlands (England)', 'West Midlands (England)', 'East (England)', 'London (England)',
                 'South East (England)', 'South West (England)', 'Wales']
    )
    income = models.StringField(
        label='What was your monthly income, before taxes, on average last year?',
        choices=['Less than £1,000', '£1,000 – £1,499', '£1,500 – £1,999', '£2,000 – £2,499', '£2,500 – £2,999',
                 '£3,000 – £3,999', '£4,000 – £6,999', 'More than £6,000', 'Prefer not to say']
    )
    origin_father = models.StringField(
        label='Where was your father born?',
        choices=['UK', 'other countries in Europe', 'Africa', 'Asia', 'US or Canada', 'Mexico or South America',
                 'Oceania', 'Prefer not to say']
    )
    origin_mother = models.StringField(
        label='Where was your mother born?',
        choices=['UK', 'other countries in Europe', 'Africa', 'Asia', 'US or Canada', 'Mexico or South America',
                 'Oceania', 'Prefer not to say']
    )
    stand = models.IntegerField(choices=range(1, 8))
    crime_worry = models.IntegerField(choices=range(1, 8))
    vote = models.BooleanField(
        widget=widgets.RadioSelect,
        label='Did you vote in the last general election?',
        choices=[(True, 'Yes'), (False, 'No')]
    )
    vote_yes = models.StringField(
        label='In the last general election, you supported:',
        choices=['Conservative Party', 'Labour Party', 'Democratic Unionist Party', 'Sinn Féin',
                 'Liberal Democrats', 'Ukip', 'Green Party', 'Plaid Cymru - Party of Wales', 'Reform UK',
                 'Other', 'Prefer not to say'],
        blank=True,
    )
    vote_no = models.StringField(
        label='Even if you did NOT vote, please indicate the party that you were most likely to have voted '
              'for or who represents your views most closely:',
        choices=['Conservative Party', 'Labour Party', 'Democratic Unionist Party', 'Sinn Féin',
                 'Liberal Democrats', 'Ukip', 'Green Party', 'Plaid Cymru - Party of Wales', 'Reform UK',
                 'Other', 'Prefer not to say'],
        blank=True,
    )

    # Manipulation check question
    control_crime = models.IntegerField(choices=range(1, 8))
    scared = likert1('Scared')
    nervous = likert1('Nervous')
    calm = likert1('Calm')
    relaxed = likert1('Relaxed')
    encouraged = likert1('Encouraged')
    discouraged = likert1('Discouraged')
    angry = likert1('Angry')
    joyful = likert1('Joyful')

    # Attention check question
    aq = models.BooleanField(
        label='',
        choices=[(True, 'Yes, I have devoted full attention to the questions so far and '
                        'I think you should use my responses for your study.'),
                 (False, 'No, I have NOT devoted full attention to the questions so far and '
                         'I think you should NOT use my responses for your study.')],
        widget=widgets.RadioSelect
    )

    # Feedback
    purpose = models.LongStringField(
        label='Do you have any idea about the purpose of this study? If yes, please briefly describe in the text field. (Optional)',
        blank=True
    )
    expcrime = models.BooleanField(
        label='Have you or your close family experienced burglary in your life? (Optional)',
        blank=True
    )
    drug_neighbor = models.IntegerField(choices=range(1, 8))
    drug_city = models.IntegerField(choices=range(1, 8))
    believe = models.BooleanField(blank=True, initial=0)
    against = models.BooleanField(blank=True, initial=0)
    conform = models.BooleanField(blank=True, initial=0)
    random = models.BooleanField(blank=True, initial=0)


# PAGES
class Introduction(Page):
    pass


class Consent(Page):
    pass


class ACvideo(Page):
    form_model = 'player'
    form_fields = ['answer']

    @staticmethod
    def error_message(player, values):
        if values['answer'] == 3169:
            return
        player.aqvideo_attempts += 1
        if player.aqvideo_attempts < 2:
            return 'You have typed in wrong digits. Please try again.'

    @staticmethod
    def before_next_page(player, timeout_happened):
        answer = player.field_maybe_none('answer')
        if answer == 3169:
            player.aqvideo = 1


class ACvideofail(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.aqvideo != 1


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'employ', 'income',
                   'region', 'origin_father', 'origin_mother', 'stand',
                   'crime_worry', 'vote', 'vote_yes', 'vote_no']


class Info1(Page):
    pass


class Info2(Page):
    pass


class Info3(Page):
    @staticmethod
    def vars_for_template(player):
        image = {
            'North East (England)': 'crime/Slide3.JPG',
            'North West (England)': 'crime/Slide4.JPG',
            'Yorkshire and The Humber (England)': 'crime/Slide5.JPG',
            'East Midlands (England)': 'crime/Slide6.JPG',
            'West Midlands (England)': 'crime/Slide7.JPG',
            'East (England)': 'crime/Slide8.JPG',
            'London (England)': 'crime/Slide9.JPG',
            'South East (England)': 'crime/Slide10.JPG',
            'South West (England)': 'crime/Slide11.JPG',
            'Wales': 'crime/Slide12.JPG',
        }
        return {
            'image': image.get(player.region),
        }


class Info4(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 'blame' or player.treatment == 'nonblame'

    @staticmethod
    def vars_for_template(player):
        image = {
            'blame': 'crime/blame.jpg',
            'nonblame': 'crime/nonblame.jpg'
        }
        return {
            'image': image.get(player.treatment),
        }


class Control(Page):
    form_model = 'player'
    form_fields = ['control_crime']


class Emotion(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        import random
        survey = ['scared', 'nervous', 'discouraged', 'encouraged', 'calm',
                  'relaxed', 'angry', 'joyful']
        random.shuffle(survey)
        return survey


class Feedback1(Page):
    form_model = 'player'
    form_fields = ['aq', 'purpose', 'AIuse', 'expcrime', 'drug_neighbor', 'drug_city']


class Feedback2(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        return [demand['name'] for demand in C.DEMAND]


class Debrief(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 'crime'


class ProlificCompletion(Page):
    pass


page_sequence = [
    Introduction, Consent,
    ACvideo,  # video attention check for bot detection
    ACvideofail,  # dead end for participants who failed the bot check twice
    Demographics,
    Info1, Info2, Info3, Info4,   # information slides
    Control, Emotion,
    Feedback1, Feedback2,
    Debrief, ProlificCompletion
]