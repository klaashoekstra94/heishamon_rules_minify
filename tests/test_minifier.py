import pytest

from heishamon_rules_minify.minifier import Minifier


def test_minifier():
    input_text = """
--[[
Multiline block comment
]]

---------------------------------- System boot ---------------------------------
on System#Boot then
    -- No problem to use long descriptive variable names
    #HeatingWaterSupplyTemperatureSetpoint = 1;
    setTimer(3, 60); -- Set timer 3 to trigger after 60s
end
  

-- Also no problem to use long descriptive function names
on CalculateWeatherDependentControl then
    -- Use comments to explain what the function should do
    $WaterTemperatureWarmWeather = 32;
    $OutsideTemperatureWarmWeather = 14;
    $WaterTemperatureColdWeather = 41;
    $OutsideTemperatureColdWeather = -4;

    #HeatingWaterSupplyTemperatureSetpoint = $WaterTemperatureWarmWeather;

    if @Outside_Temp >= $OutsideTemperatureWarmWeather then
        #HeatingWaterSupplyTemperatureSetpoint = $WaterTemperatureWarmWeather;
    elseif @Outside_Temp <= $OutsideTemperatureColdWeather then
        #HeatingWaterSupplyTemperatureSetpoint = $WaterTemperatureColdWeather;
    else
        #HeatingWaterSupplyTemperatureSetpoint =
            $WaterTemperatureWarmWeather + -- Splitting a calculation over multiple lines
                (($OutsideTemperatureWarmWeather - @Outside_Temp) *
                 -- Put comment halfway a multiline calculation
                 ($WaterTemperatureColdWeather - $WaterTemperatureWarmWeather) /
                 ($OutsideTemperatureWarmWeather - $OutsideTemperatureColdWeather));
    end
end
  
------------------------------ Thermostat triggers ----------------------------- 
on ?roomTemp then
    -- Calculate WAR when room temperature changes
    CalculateWeatherDependentControl();

    $margin = 0.25;
    $setpoint = ?roomTempSet;

--[[
    -- Put multiline comment block around script that should be ignored
    $margin = 0.5;
--]]

    if ?roomTemp > ($setpoint + $margin) then
        if @Heatpump_State == 1 then
            @SetHeatpump = 0;
        end
    elseif ?roomTemp < ($setpoint - $margin) then
        if @Heatpump_State == 0 then
            @SetHeatpump = 1;
        end
    else
        @SetZ1HeatRequestTemperature = round(#HeatingWaterSupplyTemperatureSetpoint);
    end
end
  
-------------------------------- Timer functions -------------------------------
on timer=3 then
    -- Similar variable names are each minified uniquely
    $somevalue = 0;
    $someValue = 1;
    $SomeValue = 2;
    $SoveValue3 = 3;
    $SomeValuee = 4;
    setTimer(3, 60);
end
"""

    expected_output = """on System#Boot then #HWSTS = 1;setTimer(3,60);end
on CWDC then $WTWW = 32;$OTWW = 14;$WTCW = 41;$OTCW = -4;#HWSTS = $WTWW;if @Outside_Temp >= $OTWW then #HWSTS = $WTWW;elseif @Outside_Temp <= $OTCW then #HWSTS = $WTCW;else #HWSTS = $WTWW + (($OTWW - @Outside_Temp) * ($WTCW - $WTWW) / ($OTWW - $OTCW));end end
on ?roomTemp then CWDC();$M = 0.25;$S = ?roomTempSet;if ?roomTemp > ($S + $M) then if @Heatpump_State == 1 then @SetHeatpump = 0;end elseif ?roomTemp < ($S - $M) then if @Heatpump_State == 0 then @SetHeatpump = 1;end else @SetZ1HeatRequestTemperature = round(#HWSTS);end end
on timer=3 then $S1 = 0;$SV = 1;$SV1 = 2;$SV3 = 3;$SV2 = 4;setTimer(3,60);end 
"""
    output = Minifier.minify(input_text)
    assert output == expected_output
