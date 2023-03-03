                                            
clear all;
cl=clock;                                        
KbName('UnifyKeyNames');  

[stat,struc] = fileattrib;
PathCurrent = struc.Name;% path principal
%% INTRODUCIR DATOS
subject = '1'; 
prfe=sprintf('bar_%s%s',subject);  %curso training july 2022
images_in_folder =30;                                                                                                                                                                                              
exposition_period = 15;  

size_factor=1; %factor aumento/disminucion  de la imagen original, > 1 = aumento, < 1 = disminucisn
re_escalar_imagen=0; % 1 = escalar a la resolucion de pantalla, 0 = no (se supone que ya son imagenes 2048 x 1536)
mirror_image=0; %0 = original image, 1 = mirror image 
Path_images = 'Z:\backup_antiguo_ordenador\escritorio\projects\pupil_labs\stimulus\IMAGENES\ceramicas 2014';
path_save_data = 'C:\Users\Usuario\Desktop\curso training july 2022\experiment\DATA\';
%% PARAMETERS

do_eyelink = 0; %% 0 for debugging without using eyelink; 1 for using eyelink  
display_monitor = 0;% numbers diferent than 3 are suited for a 1600X1200 pixels screen,...
                     %number 3 is for a 2048x1536 screen, if you are not
                     %using any of those comment below and set your own   
                     %screen parameters
                     %                                                                      

do_we_reCOLOR = 0; % 0 = no recoloreamos el fondo del objeto,1 = si 
    old_color=255;                                                                                    
    new_color=128;
 
type_of_experiment = 0; %0 = free viewing, 1 = multiquestions, 2 = free viewing + one question, 3 = first observations then  observation + questions. 
k = 1;% variable de avance para los bucles, con respuestas
white_or_blackground = 0; %0 = white background, 1= black background.      
contrast_factor = 1; % valores entre 0 y 1 permiten reducir el contraste de la imagen original. 
background_color = 255;           
letters_color = 0;  

sound = 0;

prf=sprintf('%s_%d_%d_%d_%s',date,cl(4),cl(5),round(cl(6)),subject);

% mkdir(path_save_data, prf);                                                
% path_exp = sprintf('%s\%s',path_save_data, prf); 
% cd(path_exp);    
%  
ImageNames_exp_0 = cell(1,images_in_folder); 
 
% PARAMETERS MAIN SCREEN
Screen('Preference','SkipSyncTests', 1);
whichScreen = display_monitor;
FrRa = FrameRate(whichScreen); 

%VTOTAL for screens at USC,
if whichScreen == 2;
    X_displayScreen = 2048;
    Y_displayScreen = 1536;
else
    X_displayScreen = 1600;
    Y_displayScreen = 1200; 
end
  
% Screen('Preference', 'VBLEndlineOverride', Y_displayScreen); 

%disp('this is Framerate')
[window,windowRect] = Screen(whichScreen,'OpenWindow', background_color,[]);
white = WhiteIndex(window); 
black = BlackIndex(window); 
gray=(white+black)/2; 
%INITIALICE KEYBOARD
escapeKey = KbName('escape');
returnKey = KbName('return');
spaceKey = KbName('space'); 

%% CREATE IMAGE TEXT FILE
% pics
exp_0_jpg = dir(sprintf('%s/*.jpg',Path_images)); 
exp_0_tif = dir(sprintf('%s/*.tif*',Path_images));
exp_0_png = dir(sprintf('%s/*.png*',Path_images));
exp_0_if = [exp_0_jpg; exp_0_tif; exp_0_png]; %get images in specified folder

if isempty(exp_0_if),
    error('No pictures for this session');
end
for i=1:length(exp_0_if)
    ImageNames_exp_0{i} = exp_0_if(i).name;
end
ImageNames_exp_0 = ImageNames_exp_0%sort(ImageNames_exp_0);
Ni_exp_0 = i;

%% MESSAGES  
    message1 = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX';%
    message2 = '       PRESIONA LA BARRA ESPACIADORA PARA CONTINUAR';
    message3 = '        ESTA PRUEBA HA CONCLUIDO !MUCHAS GRACIAS!';
    message4 = '           MIRA LAS SIGUIENTES IMAGENES'; 

%% STEP = 1
% CONECTION WITH THE EYETRACKER       
% Initialization of the connection with the Eyelink Gazetracker.
if do_eyelink == 1
    initializedummy=0;
    if initializedummy~=1
        if Eyelink('initialize') ~= 0  
            fprintf('error in connecting to the eye tracker');
            return;
        end
    else
        Eyelink('initializedummy');
    end
end

%% STEP = 2 DIALOG BOX TO SET EDF FILE NAME                 

if do_eyelink == 1
    edfFile=sprintf('%s.EDF',prfe);
end


%% STEP = 5 CREATE AND OPEN FILE FOR STORAGING DATA
f_exp_0=fopen(sprintf('ImageNames_exp_0%s.txt',prf),'w');
f_exp_01=fopen(sprintf('ImageNames_exp_01%s.txt',prf),'w');
for i=1:length(exp_0_if),
    fprintf(f_exp_0,'%s\n',ImageNames_exp_0{i});
    t=findstr('_',exp_0_if(i).name); fprintf(f_exp_01,'%s\n', ImageNames_exp_0{i}(1:end));
end
fclose(f_exp_0); fclose(f_exp_01);

%% STEP = 6 IMAGE ORDER PRESENTATION
% free viewing
aux = repmat(1:images_in_folder,1,1);
order_im_exp_0 = aux(randperm(images_in_folder));

prf=sprintf('-%s-%d-%d-%d',date,cl(4),cl(5),round(cl(6)));
f_im_order=fopen(sprintf('TrialOrder%s.txt',prf),'w');
fprintf(f_im_order,'%3d\n',order_im_exp_0); %order_im_fv es un vector no una matriz
fclose(f_im_order);

% STEP = 7.2  
% % PROVIDE EYELINK GRAPHICS ENVIRONMENT 
if do_eyelink == 1
    el=EyelinkInitDefaults(window);
    [v vs]=Eyelink('GetTrackerVersion');
    fprintf('Running experiment on a ''%s'' tracker.\n', vs );
    % open file to record data to
    
    i = Eyelink('Openfile', edfFile);
    if i~=0
        printf('Cannot create EDF file ''%s'' ', edfFile);
        Eyelink( 'Shutdown');
        return;
    end
    Eyelink('command', 'add_file_preamble_text ''Recorded by EyelinkToolbox demo-experiment''');
    %%%
    % Eyelink('command', 'add_file_preamble_text ''Recorded by EyelinkToolbox demo-experiment''');
    [width, height]=Screen('WindowSize', whichScreen);
    %window and monitor properties 
    xcenter=windowRect(3)/2;
    ycenter=windowRect(4)/2;
    Priority(1); %Enable realtime-scheduling
    ifi = Screen('GetFlipInterval', window, 200);
    Priority(0); %Disable realtime-scheduling
    frame_rate=1/ifi;
    white=WhiteIndex(window); 
    black=BlackIndex(window);
    gray=(white+black)/2;
    experiment = struct ('pwd', 'date');
    experiment.pwd=pwd;
    experiment.date=date;
    experiment.xcenter=xcenter;
    experiment.ycenter=ycenter;
    experiment.frame_duration=ifi; 
    experiment.frame_rate=frame_rate;
end

tex_exp_0=zeros(1,Ni_exp_0);


KbName('UnifyKeyNames');
A_key = KbName('a');
B_key = KbName('b');
C_key = KbName('c');
D_key = KbName('c');

rightKey = KbName('RightArrow');%keycode for FV
leftKey = KbName('LeftArrow');%keycode for FV
%Screen('Preference','SkipSyncTests',1);
Screen('Preference','VisualDebugLevel',3);
%Screen('Preference', 'SuppressAllWarnings', 1); 
AssertOpenGL;    % Running on PTB-3? Abort otherwise.
 
%% STEP = 7 IMAGES
scal_factor=X_displayScreen/Y_displayScreen;%default

for i=1:Ni_exp_0, 
    ImageNames_exp_0(i)
    %         images_4_presentation(Im,Y_displayScreen, X_displayScreen, do_we_resize,ImageNames_exp_0{i});
    
    Im=imread(sprintf('%s/%s',Path_images,ImageNames_exp_0{i})); 
    %convierte a rgb si si
    if size(Im,3)==1 
        Im(:,:,2)=Im(:,:,1);
    end
    if size(Im,3)==2
        Im(:,:,3)=Im(:,:,2);
    end
    
    if mirror_image == 1
        Im2(:,:,1)=fliplr(Im(:,:,1));
        Im2(:,:,2)=fliplr(Im(:,:,2));
        Im2(:,:,3)=fliplr(Im(:,:,3));
        Im=Im2;
        Im2=[];
    end
    
    if re_escalar_imagen==1
        cd(PathCurrent);  
        [Im2]  = escala_imagen(Im,Y_displayScreen,X_displayScreen,background_color ,size_factor);
        cd(path_exp);  
    else
        Im2=Im;
    end
    if do_we_reCOLOR==1 
        cd(PathCurrent);
        [Im2] = recolorear_fondo_objeto(Im2,old_color,new_color);
        cd(path_exp);  
    end
    
    nRows=size(Im2,1); nCols=size(Im2,2);
    imageRect_exp_0{i}=SetRect(0,0,nCols,nRows); 
    destRect_exp_0{i}=CenterRect(imageRect_exp_0{i},windowRect);    
    w_exp_0(i)=Screen('MakeTexture',window,Im2,background_color);
    %Screen('DrawText   ure',window,w_exp_0(i),imageRect_exp_0{i},destRect_exp_0{i});   
    %imwrite(Im, sprintf('test%d.jpg', n));
        filename = sprintf('image_%s', ImageNames_exp_0{i}); 
%         filename = sprintf('espejo_image_%s', ImageNames_exp_0{i}); 
    imwrite(Im2, filename);  
    %image_name = sprintf('%s',ImageNames_exp_0{i});
    %imwrite(Im, 'image%s',image_name);
end

%% STEP = 9 SET UP TRACKER CONFIGURATION 
if do_eyelink == 1
    % Setting the proper recording resolution, proper calibration type,
    % as well as the data file content;
    Eyelink('command','screen_pixel_coords = %ld %ld %ld %ld', 0, 0, width-1, height-1);
    Eyelink('message', 'DISPLAY_COORDS %ld %ld %ld %ld', 0, 0, width-1, height-1);
    % set calibration type.
    % CPG: Matias mentioned using only the 5 points calibration
    %     Eyelink('command', 'calibration_type = HV5');
    Eyelink('command', 'calibration_type = HV9') 
    % set parser (conservative saccade thresholds)
    Eyelink('command', 'saccade_velocity_threshold = 35');
    Eyelink('command', 'saccade_acceleration_threshold = 9500');
    % set EDF file contents
    Eyelink('command', 'file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON');%% we could eliminate some of the
    %warning messages in order to clear the code for working with matlab(fixation, saccade, blink, and button messages)
    %but it would cause the data viewer to work unproperly.
    Eyelink('command', 'file_sample_data  = LEFT,RIGHT,GAZE,HREF,AREA,GAZERES,STATUS');
    % set link data (used for gaze cursor)
    Eyelink('command', 'link_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON');
    Eyelink('command', 'link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS');
    % allow to use the big button on the eyelink gamepad to accept the
    % calibration/drift correction target
    Eyelink('command', 'button_function 5 "accept_target_fixation"');% it would be desirable to use the axisbutton for accepting
    %calibrations. at least during the drift correction intercalated while the experiment is running
    % make sure we're still connected.
    mouseInsteadOfGaze=0; %control gaze cursor using mouse instead of gaze (for testing, in case calibration isn't worked out yet)
    if Eyelink('IsConnected')~=1 
        return;
    end;
end

%%  STEP = 10 CALIBRATE THE EYETRACKER
% % setup the proper calibration foreground and background colors 
if do_eyelink == 1
    el.backgroundcolour = 128;           
    el.foregroundcolour = 0;     
    HideCursor;
    Screen('HideCursorHelper', window);
    EyelinkDoTrackerSetup(el);
end

background = Screen('MakeTexture',window, background_color, background_color);  

%% WRITING THE MESSAGE TO PUT AT THE BEGINING OF THE EXPERIMENT 
Screen('TextSize',window, 30);
Screen('TextStyle', window, 0);

Screen('DrawText', window, double(message1), 350, windowRect(4)/2-40, letters_color,  background_color);
Screen('Flip',window);
WaitSecs(0.1);    

[touch, secs, keyCode] = KbCheck;
  
while ~keyCode(spaceKey), [touch, secs, keyCode] = KbCheck; end
Screen('DrawTexture',  window, background)
Screen('Flip',window);

%% STEP = 11 EXPERIMENT PRESENTATION
  
k = 1;% variable de avance para los bucles, con respuestas

    % FREE OBSERVATION 
    % THIS OPTION SHOWS FIRST ALL THE IMAGES FOR FREE PRESETNATION THEN
    % THE DIFFERENT IMAGES WITH CORRESPONDING QUESTIONS
    %
    iorder_exp_0 = 0;
    for i=1:length(order_im_exp_0)
        i        
        iorder_exp_0 = iorder_exp_0 + 1;
        
        if iorder_exp_0 == 1   
                Screen('DrawText', window, double(message4), 400, windowRect(4)/2-40, letters_color,  background_color);
                Screen('Flip',window);
                WaitSecs(3);
        end
        %start eyetracker
        if do_eyelink == 1
            Eyelink('command', 'record_status_message "TRIAL %d/%d"', i, length(iorder_exp_0));
            WaitSecs(0.1);
            EyelinkDoDriftCorrection(el);
            Eyelink('Command', 'set_idle_mode');
            WaitSecs(0.1);
            
            Eyelink('StartRecording', 1, 1, 1, 1);
            WaitSecs(0.1);
%             Eyelink('Message', 'IMAGE: %d', ImageNames_exp_0(iorder_exp_0));
%             WaitSecs(0.1);
            Eyelink('Message', 'START TRIAL: %d', order_im_exp_0(iorder_exp_0));
            
%             Eyelink('Message', 'FREE VIEWING %d%d', i, exposition_period     );
        end
        Screen('DrawTexture',window,w_exp_0(order_im_exp_0(iorder_exp_0)),imageRect_exp_0{order_im_exp_0(iorder_exp_0)},destRect_exp_0{order_im_exp_0(iorder_exp_0)});
        
        Screen('Flip', window);
        WaitSecs(exposition_period);
        
        if do_eyelink == 1       
            Eyelink('Command', 'set_idle_mode');
            Eyelink('StopRecording');
%             EyelinkDoDriftCorrection(el);
        end

        if iorder_exp_0 < images_in_folder
            if do_eyelink == 0 
                Screen('DrawText', window, double(message2), 400, windowRect(4)/2-40, letters_color,  background_color);
                Screen('Flip',window);
                WaitSecs(0.2);
%                 [touch, secs, keyCode] = KbCheck;
                while ~keyCode(spaceKey), [touch, secs, keyCode] = KbCheck;end
                Screen('DrawTexture',  window, background)
                Screen('Flip',window);
            end
            
        else
            Screen('DrawText', window, double(message3), 350, windowRect(4)/2-40, letters_color, background_color);
            Screen('Flip',window);
            WaitSecs(5);
        end
    end 
    

Screen('CloseAll')


%%     STEP = 12 END OF THE EXPERIMENT
Priority(0);
ShowCursor;

if do_eyelink == 1
    Eyelink('Command', 'set_idle_mode');
    WaitSecs(0.5);
    Eyelink('CloseFile');
    % download data file
    try
        fprintf('Receiving data file ''%s''\n', edfFile );
        status=Eyelink('ReceiveFile');
        if status > 0
            fprintf('ReceiveFile status %d\n', status);
        end
        if 2==exist(edfFile, 'file')
            fprintf('Data file ''%s'' can be found in ''%s''\n', edfFile, pwd );
        end
    catch
        fprintf('Problem receiving data file ''%s''\n', edfFile );
    end
    %close the eye tracker.
    Eyelink('ShutDown');
end


                 

