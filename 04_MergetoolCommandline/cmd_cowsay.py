import os
import cowsay
import readline
import shlex
import cmd
from pathlib import Path


def parse(args):
    return shlex.split(args)


def get_args(args):
    opt_args = dict(zip(args[0::2], args[1::2]))
    return opt_args


def get_final_args(args, default_args):
    for key, value in default_args.items():
        if key not in args.keys():
            args[key] = value

    return args


def complete(text, line, begidx, endidx):
    cow_say = cow_think = {"-e": ["oo", "xx", "@@", "HH", "**", "cc", "00", "++"],
                         "-c": cowsay.list_cows(),
                         "-T": ["  ", "--", "==", "ll", "//"]}

    bubble = {"-b": ["cowsay", "cowthink"], "-w": ["true", "false"]}

    variants = {'cowsay': cow_say, 'cowthink': cow_think, 'make_bubble': bubble}
    key, command = shlex.split(line)[-1] if begidx == endidx else shlex.split(line)[-2], shlex.split(line)[0]
    return [s for s in variants[command][key] if s.startswith(text)]


class Cowsay(cmd.Cmd):
    intro = 'Welcome to Cowsay terminal'
    prompt = 'Cowsay >>>> '

    def do_cowsay(self, args):
        '''
        Return the resulting cowsay string

        cowsay message [-e eye_string] [-c cow] [-T tongue_string]

        message: The message to be displayed
        cow: the available cows can be found by calling "list_cows"
        eye_string: eye string
        tongue_string: tongue string
        '''

        try:
            message, *opt_args = parse(args)

            if len(opt_args) == 1:
                raise Exception

            opt_args = get_args(opt_args)
            default_args = {'-c': 'default', '-e': cowsay.Option.eyes, '-T': cowsay.Option.tongue}
            opt_args = get_final_args(opt_args, default_args)

            if len(opt_args) > 3:
                raise Exception

            if opt_args['-c'] not in cowsay.list_cows():
                print("Inputed cow not in cow list")
                return

            print(cowsay.cowsay(message, cow=opt_args['-c'], eyes=opt_args['-e'][:2], tongue=opt_args['-T'][:2]))
        except Exception:
            print("Invalid function parameters\nTo view help, enter \"help cowsay\"")

    def complete_cowsay(self, text, line, begidx, endidx):
        return complete(text, line, begidx, endidx)

    def do_cowthink(self, args):
        '''
        Return the resulting cowthink string

        cowsay message [-e eye_string] [-c cow] [-T tongue_string]

        message: The message to be displayed
        cow: the available cows can be found by calling "list_cows"
        eye_string: eye string
        tongue_string: tongue string
        '''

        try:
            message, *opt_args = parse(args)

            if len(opt_args) == 1:
                raise Exception

            opt_args = get_args(opt_args)
            default_args = {'-c': 'default', '-e': cowsay.Option.eyes, '-T': cowsay.Option.tongue}
            opt_args = get_final_args(opt_args, default_args)

            if len(opt_args) > 3:
                raise Exception

            if opt_args['-c'] not in cowsay.list_cows():
                print("Inputed cow not in cow list")
                return

            print(cowsay.cowthink(message, cow=opt_args['-c'], eyes=opt_args['-e'][:2], tongue=opt_args['-T'][:2]))
        except Exception:
            print("Invalid function parameters\nTo view help, enter \"help cowsay\"")

    def complete_cowthink(self, text, line, begidx, endidx):
        return complete(text, line, begidx, endidx)

    def do_list_cows(self, args):
        '''
        Lists all cow file names in the given directory

        list_cows [path]

        path: path to the directory with cow files
        '''

        try:
            arguments = parse(args)

            if len(arguments) > 1:
                raise Exception

            path = arguments[0] if arguments else cowsay.COW_PEN

            if not Path(path).is_dir():
                print("No such directory")
                return

            cow_list = cowsay.list_cows(path)
            if cow_list:
                print(*cow_list, sep='\n')
        except Exception:
            print("Invalid function parameters\nTo view help, enter \"help list_cows\"")

    def complete_list_cows(self, text, line, begidx, endidx):
        string = shlex.split(line)[-1]
        new_string = string.rsplit('/', 1)[0]
        if new_string == '':
            new_string = '/'
        paths = [str(elem).split('/')[-1] for elem in Path(new_string).iterdir() if elem.is_dir()]
        return [s + '/' for s in paths if s.startswith(text)]

    def do_make_bubble(self, args):
        '''
        Wraps text is wrap_text is true, then pads text and sets inside a bubble.
        This is the text that appears above the cows

        make_bubble text [-b brackets] [-W width] [-w wrap_text]

        text: text in bubble
        brackets: "cowsay" or "cowthink" string
        width: width of field (number)
        wrap_text: "true" or "false" string
        '''

        try:
            message, *opt_args = parse(args)

            if len(opt_args) == 1:
                raise Exception

            opt_args = get_args(opt_args)
            default_args = {'-b': 'cowsay', '-W': 40, '-w': True}
            opt_args = get_final_args(opt_args, default_args)

            if len(opt_args) > 3:
                raise Exception

            if not str(opt_args['-W']).isdigit():
                raise Exception

            if opt_args['-b'] != 'cowsay' and opt_args['-b'] != 'cowthink':
                raise Exception

            if opt_args['-w'] == 'true':
                opt_args['-w'] = True
            elif opt_args['-w'] == 'false':
                opt_args['-w'] = False
            elif not isinstance(opt_args['-w'], bool):
                raise Exception

            print(cowsay.make_bubble(message, brackets=cowsay.THOUGHT_OPTIONS[opt_args['-b']],
                                     width=int(opt_args['-W']), wrap_text=opt_args['-w']))
        except Exception:
            print("Invalid function parameters\nTo view help, enter \"help make_bubble\"")

    def complete_make_bubble(self, text, line, begidx, endidx):
        return complete(text, line, begidx, endidx)

    def do_clear(self, args):
        '''
        Clear Cowsay command line window

        clear
        '''

        if len(args) > 0:
            print("Invalid function parameters\nTo view help, enter \"help clear\"")
            return 0

        os.system('clear')

    def do_exit(self, args):
        '''
        Exit from Cowsay command line

        exit
        '''

        if len(args) > 0:
            print("Invalid function parameters\nTo view help, enter \"help exit\"")
            return 0

        return 1


if __name__ == "__main__":
    os.system('clear')
    Cowsay().cmdloop()