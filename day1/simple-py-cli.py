import argparse



# get input from user
parser = argparse.ArgumentParser(description="A simple CLI that take name and company and print data")
parser.add_argument("--name", type=str, required=True, help="Your name")
parser.add_argument("--age", type=int, required=True, help="Your age")
parser.add_argument("--company", type=str, required=True, help="Your company name")
parser.add_argument("--hobbies", type=str,nargs="+", required=False, help="hobbies(optional)", default=[] )


args = parser.parse_args()
# print(args)
name = args.name
age =  args.age
company = args.company
hobbies = args.hobbies


print(f"{name} is a {age} years old guy working for {company}")
if len(hobbies) > 0:
    print(f"{name} has the following hobbies: {hobbies}")

# print("Parsing arguments...")