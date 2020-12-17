## Homes :

    SET INT Home_Number

    SET FLOAT initial_production : random between 0 and 1 

    SET FLOAT consumption_rate : random between 0 and 1 

    SET INT energy_trade_policy : random in {0,1,2} 

    FOR EACH Day :

      READ Temperature_actual(T1) and Temperature_before(T2) in the shared memory

      SET consumption_rate = consumption_rate - ((T1 - T2)/100)

      SET FLOAT Energy_amount = initial_production - consumption_rate

      IF Energy_amount >= 0

        SET Message = (0,Energy_available,Home_Number)
    
        IF energy_trade_policy == 0 OR energy_trade_policy == 2

          PUT Message in Queue Home/Home

        ELSEIF energy_trade_policy == 2 AND timer Message END

        DELETE Message in Queue Home/Home

        PUT Message in Queue Market/Home

        ELSE IF energy_trade_policy == 1

        PUT Message in Queue Market/Home

        ENDIF

      ELSE
  
        CHECK Queue Home/Home

        IF one_message = (0,Energy_available,Home_Number) AND Energy_available >= Energy_amount

          GET one_message

          Energy_amount = Energy_amount + Energy_available

        ELSE 

           SET Message = (1, Energy_amount, Home_Number) 

           PUT Message in Queue Market/Homes

        ENDIF

      ENDIF

    ENDFOR

## Weather :

    SET FLOAT T = 18,25

    SET INT Compteur = -1

    FOR EACH Day
    
      SET FLOAT Probability = random between 0,0 and 1,0 

      T = T+ Compteur * 0,05 

      IF T == 36,5

        Compteur = -1

      ELSE IF T == 0

        Compteur = 1

      ENDIF

      PUT T in Shared_Memory

      FOR EACH natural-disaster

        IF Probability < Probability_Natural_Disaster

          PUT natural-disaster IN Shared_Memory 

        ENDIF

      ENDFOR

    ENDFOR

## Market :

    SET FLOAT Energy_Price = 0,1

    SET FLOAT Energy_In = 0

    SET FLOAT Energy_Out = 0

    SET FLOAT Long_Term_Coeff = 0,0001
    
    SET INT Max_Thread = 3

    FOR EACH Day

      SET INT Thread_Count = 0

      CATCH Signals (FROM Economics and Politics)

      READ Temperature AND Natural_Disaster FROM Shared-Memory

      CHECK Queue Market/Home

      FOR EACH one_Message in Queue Market/Home

        IF Thread_Count <= Max_Thread 

          IN A SEPARATE THREAD :

          IF one_Message == (0, Energy_available, Home_Number)

            Energy_In = Energy_In + Energy_available

          ELSE IF one_Message == (1, Energy_amount, Home_Number) 

            Energy_Out = Energy_Out + Energy_Amount

          ENDIF

        ENDIF

      ENDFOR

      Energy_Difference = Energy_In-Energy_Out

      Energy_Price = formula Energy_Price (depends on Economics and Politics Signals, Long_Term_Coeff, Temperature, Happening of Natural Disaster, Energy_difference, previous Energy_Price, )

      Update Terminal : Print (Energy_Price)
   
    ENDFOR

## Economics and Politics :

    SET FLOAT Probability = random between 0 and 1

    FOR EACH Day	

      FOR EACH Event 

        IF Probability < Probability_Event

          SEND SIGNAL (Event)

        ENDIF

      ENDFOR

    ENDFOR

## Main Process :

    MULTIPROCESSING (in this order) :

    WHILE True 

      BEGIN New Day

      RUN as MULTIPROCESSES :

        * Weather

        * Economics and Politics 

        * Wait Weather, Economics and Politic THEN RUN Homes

        * WAIT Homes THEN RUN Market

      END Day

  
