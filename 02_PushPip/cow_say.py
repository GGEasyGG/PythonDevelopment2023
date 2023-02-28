import argparse
import cowsay


parser = argparse.ArgumentParser()
parser.add_argument('message', nargs='?', default=None)
parser.add_argument('-e', dest='eyes', default=cowsay.Option.eyes, type=str)
parser.add_argument('-f', dest='cowfile', default=None, type=str)
parser.add_argument('-l', dest='l', action='store_true')
parser.add_argument('-n', dest='wrap', action='store_true')
parser.add_argument('-T', dest='tongue', default=cowsay.Option.tongue, type=str)
parser.add_argument('-W', dest='width', default=40, type=int)
parser.add_argument('-b', dest='b', action='store_true')
parser.add_argument('-d', dest='d', action='store_true')
parser.add_argument('-g', dest='g', action='store_true')
parser.add_argument('-p', dest='p', action='store_true')
parser.add_argument('-s', dest='s', action='store_true')
parser.add_argument('-t', dest='t', action='store_true')
parser.add_argument('-w', dest='w', action='store_true')
parser.add_argument('-y', dest='y', action='store_true')

args = parser.parse_args()

if args.l:
    print(*cowsay.list_cows(), sep=', ')
else:
    if args.message is None:
        print("Input message:")
        text = input()
        args.message = text

    if args.cowfile is not None:
        if '/' in args.cowfile:
            file = open('.' + args.cowfile, 'r')
            str = file.read()
            file.close()
            cow, args.cowfile = 'default', str
        else:
            cow, args.cowfile = args.cowfile, None
    else:
        cow = 'default'

    preset = None
    for elem in 'bdgpstwy':
        if vars(args)[elem]:
            preset = elem
            break

    print(cowsay.cowsay(message=args.message, cow=cow, eyes=args.eyes[:2], tongue=args.tongue[:2], wrap_text=args.wrap,
                        width=args.width, cowfile=args.cowfile, preset=preset))
