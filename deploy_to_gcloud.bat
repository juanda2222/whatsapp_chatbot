
@echo off
setlocal

::-------------------------
:: create the schedule job:
::-------------------------

:: read messages one a day at 00:00 hour's

:scheduler_command
call gcloud scheduler jobs create pubsub readAndRespondMessagesSignal ^
    --schedule="0 0 * * *" ^ 
    --topic=read_and_respond_wa_messages ^
    --message-body="Robot is up and ready to read the messages" 

::handle the schedule error:
set next=func_deploy_command
set error_message=Scheduler creation Falied
if ERRORLEVEL 1 goto input_check


::--------------------------------------------------------------------
:: this command creates the function and the topic if it doesnt exists
::--------------------------------------------------------------------

:func_deploy_command
call gcloud functions deploy firestore_backup_bigquery ^
    --runtime python37  ^
    --source="%cd%\\..\\firestore_backup_bigquery" ^
    --trigger-topic read_and_respond_wa_messages ^
    --set-env-vars PRODUCTION=True ^
    --retry ^
    --timeout=400s

::handle the schedule error:
set error_message=Cloud function creation falied
set next=cleanup
if ERRORLEVEL 1 goto input_check


::cleanup
:cleanup
echo Server installation finished!
pause

::end routine:
:end
endlocal
::clean all error flags:
exit /b 0


:: --------- the user input handler:----------
:input_check
:: if -y was in the arguments go automaticly to next command
if "%1" == "-y" ( 
    type nul
    goto :%next% 

:: manualy check the logic on error
) else @echo (
    set input=
    set /p input="Error: %error_message%, do you still want to continue? y/n:"
    if "%input%" == "y" ( 
        type nul
        goto :%next% 
    ) else if "%input%" == "n" (
        goto :end
    ) else @echo "Option not recognized, try again!" (
        goto :input_check
    )
)