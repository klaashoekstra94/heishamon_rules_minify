import pytest

from heishamon_rules_minify.minifier import Minifier

input_text = """
--[[
Multiline block comment
]]

---------------------------------- System boot ---------------------------------
on System#Boot then
    -- No problem to use long descriptive variable names
    #HeatingWaterSupplyTemperatureSetpoint = 1;
    #allowSetQuietMode = 0;
    #quietModeHelper = 1;
    #quietModePrevious = -1;

    setTimer(3, 60); -- Set timer 3 to trigger after 60s
end
  
------------------------------- Custom functions -------------------------------
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
    else
        if @Outside_Temp <= $OutsideTemperatureColdWeather then
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
end

on setQuietMode then
    if #allowSetQuietMode == 1 then
        if isset(@Outside_Temp) && isset(@Heatpump_State) then
            if #quietModeHelper == 1 then
                if @Outside_Temp < 13 then
                    #quietMode = 1;
                else
                    #quietMode = 2;
                end
                if @Outside_Temp < 8 then
                    #quietMode = 0;
                end
                if @Outside_Temp < 2 then
                    if %hour > 22 || %hour < 7 then
                        #quietMode = 1;
                    else
                        #quietMode = 0;
                    end
                end
                if #quietModePrevious != #quietMode && @Heatpump_State == 1 then
                    setTimer(2, 900);
                    #quietModeHelper = 0;
                    #quietModePrevious = #quietMode;
                    @SetQuietMode = #quietMode;
                end
            end
        end
    end
end

------------------------------ Thermostat triggers ----------------------------- 
on ?roomTemp then
    -- Calculate WAR when room temperature changes
    --CalculateWeatherDependentControl();

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
    else
        if ?roomTemp < ($setpoint - $margin) then
            if @Heatpump_State == 0 then
                @SetHeatpump = 1;
            end
        else
            @SetZ1HeatRequestTemperature = round(#HeatingWaterSupplyTemperatureSetpoint);
        end
    end
end

-------------------------------- Timer functions -------------------------------

on timer=2 then
    #quietModeHelper = 1;
    #quietMode = 0;
end

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


def test_minifier():
    expected_output = """on System#Boot then #HWSTS = 1;#ASQM = 0;#QMH = 1;#QMP = -1;setTimer(3,60);end
on CWDC then $WTWW = 32;$OTWW = 14;$WTCW = 41;$OTCW = -4;#HWSTS = $WTWW;if @Outside_Temp >= $OTWW then #HWSTS = $WTWW;else if @Outside_Temp <= $OTCW then #HWSTS = $WTCW;else #HWSTS = $WTWW + (($OTWW - @Outside_Temp) * ($WTCW - $WTWW) / ($OTWW - $OTCW));end end end
on SQM then if #ASQM == 1 then if isset(@Outside_Temp) && isset(@Heatpump_State) then if #QMH == 1 then if @Outside_Temp < 13 then #QM = 1;else #QM = 2;end if @Outside_Temp < 8 then #QM = 0;end if @Outside_Temp < 2 then if %hour > 22 || %hour < 7 then #QM = 1;else #QM = 0;end end if #QMP != #QM && @Heatpump_State == 1 then setTimer(2,900);#QMH = 0;#QMP = #QM;@SetQuietMode = #QM;end end end end end
on ?roomTemp then $M = 0.25;$S = ?roomTempSet;if ?roomTemp > ($S + $M) then if @Heatpump_State == 1 then @SetHeatpump = 0;end else if ?roomTemp < ($S - $M) then if @Heatpump_State == 0 then @SetHeatpump = 1;end else @SetZ1HeatRequestTemperature = round(#HWSTS);end end end
on timer=2 then #QMH = 1;#QM = 0;end
on timer=3 then $S1 = 0;$SV = 1;$SV1 = 2;$SV3 = 3;$SV2 = 4;setTimer(3,60);end
"""
    output = Minifier.minify(input_text)
    assert output == expected_output

def test_minifier_comments_only():
    expected_output = """on System#Boot then
    #HeatingWaterSupplyTemperatureSetpoint = 1;
    #allowSetQuietMode = 0;
    #quietModeHelper = 1;
    #quietModePrevious = -1;

    setTimer(3, 60);end
  
on CalculateWeatherDependentControl then
    $WaterTemperatureWarmWeather = 32;
    $OutsideTemperatureWarmWeather = 14;
    $WaterTemperatureColdWeather = 41;
    $OutsideTemperatureColdWeather = -4;

    #HeatingWaterSupplyTemperatureSetpoint = $WaterTemperatureWarmWeather;

    if @Outside_Temp >= $OutsideTemperatureWarmWeather then
        #HeatingWaterSupplyTemperatureSetpoint = $WaterTemperatureWarmWeather;
    else
        if @Outside_Temp <= $OutsideTemperatureColdWeather then
            #HeatingWaterSupplyTemperatureSetpoint = $WaterTemperatureColdWeather;
        else
            #HeatingWaterSupplyTemperatureSetpoint = $WaterTemperatureWarmWeather + (($OutsideTemperatureWarmWeather - @Outside_Temp) * ($WaterTemperatureColdWeather - $WaterTemperatureWarmWeather) / ($OutsideTemperatureWarmWeather - $OutsideTemperatureColdWeather));
        end
    end
end

on setQuietMode then
    if #allowSetQuietMode == 1 then
        if isset(@Outside_Temp) && isset(@Heatpump_State) then
            if #quietModeHelper == 1 then
                if @Outside_Temp < 13 then
                    #quietMode = 1;
                else
                    #quietMode = 2;
                end
                if @Outside_Temp < 8 then
                    #quietMode = 0;
                end
                if @Outside_Temp < 2 then
                    if %hour > 22 || %hour < 7 then
                        #quietMode = 1;
                    else
                        #quietMode = 0;
                    end
                end
                if #quietModePrevious != #quietMode && @Heatpump_State == 1 then
                    setTimer(2, 900);
                    #quietModeHelper = 0;
                    #quietModePrevious = #quietMode;
                    @SetQuietMode = #quietMode;
                end
            end
        end
    end
end

on ?roomTemp then

    $margin = 0.25;
    $setpoint = ?roomTempSet;

    if ?roomTemp > ($setpoint + $margin) then
        if @Heatpump_State == 1 then
            @SetHeatpump = 0;
        end
    else
        if ?roomTemp < ($setpoint - $margin) then
            if @Heatpump_State == 0 then
                @SetHeatpump = 1;
            end
        else
            @SetZ1HeatRequestTemperature = round(#HeatingWaterSupplyTemperatureSetpoint);
        end
    end
end

on timer=2 then
    #quietModeHelper = 1;
    #quietMode = 0;
end

on timer=3 then
    $somevalue = 0;
    $someValue = 1;
    $SomeValue = 2;
    $SoveValue3 = 3;
    $SomeValuee = 4;
    setTimer(3, 60);
end
"""
    output = Minifier.minify(input_text, comments_only=True)
    assert output == expected_output
