with Text_Io;
procedure Video_Poker_Calc is
   use Text_Io;
   
   -- Instantiate standard generic I/O packages for Ada 83
   package Float_Io is new Text_Io.Float_Io(Float);
   package Int_Io is new Text_Io.Integer_Io(Integer);
   use Float_Io, Int_Io;
   RTP_Pct        : Float; -- Return-to-player %. 
   Variance       : Float; -- Game Variance
   Covariance     : Float; -- Game Multi-hand covariance
   Max_Credits    : Float;
   Bonus_Type     : Integer;
   Denom          : Float;   -- 0.1, 0.25, 0.5, 1.0, 2.0, 5.0
   N_Hands        : Float; -- 1, 3, 5, 10
   Target_Odds    : Float; --400:quads, 90:full-house, 30: super-times-pay-multiplier
   
   Guarantee_Factor : Float := 2.9; -- log(1 - %-Confidence)/log(1 - Target-Odds) / Odds. Approximately 2.9 for odds > 90
   
   Bet            : Float;
   N_Rounds       : Float;
   House_Edge     : Float; -- Entered as a %, converted to a decimal
   
   
   Var_Per_Round  : Float; -- e.g., 4.42 for 9/6 Jacks or Better
   Total_Variance : Float; 
   Z_Score        : Float:= 1.645; -- 95% Left-Sided Z-Score for % confidence of covering losses
   Exp_Loss       : Float;
   Total_Std      : Float;
   Volatility_Buffer : Float;
   Bankroll       : Float;
   
   --- store game info
   -- bonus-type, number, rtp, single-hand variance, multi-hand covariance 
   -----------------------------------------------------------
   -- bonus,               0,  99.17%, 20.91, 2.08
   -- double-double-bonus, 1,  98.98%, 41.90, 4.15
   -- triple-double-bonus, 2,  98.15%, 98.30, 9.72
   -- deuces-wild,         3,  97.06,  25.80, 2.54
   type Float_Array is array (0 .. 3) of Float;
   RTP_Pct_Array : Float_Array := ( 99.1,  98.98, 98.15, 97.06);
   Var_Pct_Array : Float_Array := ( 20.91, 41.90, 98.30, 25.80);
   Cov_Pct_Array : Float_Array := ( 2.08,  4.15,  9.72,   2.54);

   -- Portable square root function using Babylonian method for Ada 83 compatibility
   function Sqrt(X : Float) return Float is
      X0 : Float := X / 2.0;
   begin
      if X <= 0.0 then
         return 0.0;
      end if;
      for I in 1 .. 25 loop
         X0 := 0.5 * (X0 + X / X0);
      end loop;
      return X0;
   end Sqrt;
 

begin
   -- Gather User Inputs
   Put_Line("Enter Game's Max_Credit, Bonus-Type(0:b,1:ddb,2:tdb,3:dw), Denom, N-Hands, Target-Odds: ");
   New_Line;
   Get(Max_Credits);
   Get(Bonus_Type);
   Get(Denom);
   Get(N_Hands);
   Get(Target_Odds);
   
   -- Get data rom bonus type
   RTP_Pct := RTP_Pct_Array(Bonus_Type);
   Variance := Var_Pct_Array(Bonus_Type);
   Covariance := Cov_Pct_Array(Bonus_Type);
   
   -- Calculate the Rounds for Drawing target hand with 95% guarantee
   N_Rounds := Target_Odds * Guarantee_Factor / N_Hands;

   -- Perform Risk and Bankroll Calculations
   Bet := Max_Credits * Denom * N_Hands;
   House_Edge := 1.0 - RTP_Pct / 100.0;
   Exp_Loss := Bet * N_Rounds * House_Edge;
   
   Var_Per_Round := N_Hands * Variance + N_Hands * (N_Hands - 1.0) * Covariance;
   Total_Variance := N_Rounds * Var_Per_Round;
   Total_Std := Sqrt(Total_Variance);
   Volatility_Buffer   := Z_Score * Max_Credits * Denom * Total_Std;
   
   Bankroll := Exp_Loss + Volatility_Buffer;

   -- Output Results
   New_Line;
   Put_Line("========================================");
   Put_Line("          VIDEO POKER REPORT            ");
   Put_Line("========================================");
   
   Put("Bet:               $"); 
   Put(Bet, Fore => 6, Aft => 2, Exp => 0); 
   New_Line;
   
   Put("Number of Rounds:  $"); 
   Put(N_Rounds, Fore => 6, Aft => 2, Exp => 0); 
   New_Line;
   
   Put("Expected Loss:     $"); 
   Put(Exp_Loss, Fore => 6, Aft => 2, Exp => 0); 
   New_Line;
   
   Put("Volatility Buffer: $"); 
   Put(Volatility_Buffer, Fore => 6, Aft => 2, Exp => 0); 
   New_Line;
   
   Put("Required Bankroll: $"); 
   Put(Bankroll, Fore => 6, Aft => 2, Exp => 0); 
   New_Line;
   
   Put_Line("========================================");
end Video_Poker_Calc;