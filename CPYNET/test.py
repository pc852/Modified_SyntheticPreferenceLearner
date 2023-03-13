from simple_cpynet import SimpleCPnet

def main():
    temp = SimpleCPnet()
    temp.load("test.xml")
    induced = temp.induced()
    induced.print_graph()
    for incomp in induced.incomparable():
        print str(incomp[0]),"||",str(incomp[1])
        print temp.lex_eval_compare([incomp[0],incomp[1]])

main()
