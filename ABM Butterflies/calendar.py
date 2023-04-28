from contextlib import redirect_stdout
import io

class Calendar:

    @staticmethod
    def printCalendar(sim: 'simulus.simulator') -> None:
        ''' Static method to reformat the printed output of simulus's
            show_calendar() method.  This method grabs the printed output
            of sim.show_calendar and removes any extraneous (for the
            current context) information (e.g., simulator address).
        Parameters:
            sim: a simulus.simulator() object
        '''
        # grab sim.show_calendar's printed output and clean up a bit
        f = io.StringIO()
        with redirect_stdout(f):
            sim.show_calendar()
        results = f.getvalue().strip() 
        events = results.split('\n')
    
        # list of all future events (num=3) at time 4.13222 on simulator 'f0656f02-829f-8f19-36d0-a4f466f9a833':
        # 4.30296: dir_evt=arrival()
        # 4.46498: dir_evt=move()
        # 5.00415: dir_evt=move()
        equal = events[0].index('='); right_paren = events[0].index(')', equal)
        num_events = events[0][equal + 1 : right_paren]
        time_start = events[0].index("time ", right_paren) + len("time ")
        time_end   = events[0].index(' ', time_start)
        time       = events[0][time_start:time_end]
        print(f"\tCalendar (# events = {num_events} @ time {time}):")
        for i in range(1, len(events), 1):
            print(f"\t   {events[i].replace('dir_evt=','')}")

        input("Press return...")

