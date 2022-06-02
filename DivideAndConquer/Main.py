import Country as C
import State as S

def main():

    # S_obj = S.State('Andhra Pradesh')
    # S_obj.optimal_state()
    # S_obj.__del__()
    # S_obj2 = S.State('Kerala')
    # S_obj2.optimal_state()
    # S_obj2.__del__()
    S_obj3 = S.State('Tamil Nadu')
    S_obj3.optimal_state()
    S_obj3.__del__()

    C_obj = C.Country()
    #C_obj.solve_all_states()
    C_obj.optimal_route()

if __name__ == '__main__':
    main()