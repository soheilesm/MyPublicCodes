clear all
close all
clc


starttimesec = starttime/1000;
endtimesec = endtime/1000;

unixtotime = @(time) datestr( 719529 + time/86400, 'dd-mmm-yyyy HH:MM:SS');
starttimeday = zeros(1, length(starttime));
endtimeday = zeros(1, length(starttime));

for i = 1:length(starttimesec)
    starttimeday(i) = datenum(unixtotime(starttimesec(i)));
    endtimeday(i) = datenum(unixtotime(endtimesec(i)));
end

starttimeday = starttimeday - starttimeday(1) + 1;
endtimeday = endtimeday - starttimeday(1) + 1;

% firetot = zeros(1, endtimeday(end));
% 
% for i = 1:length(starttimeday)
%     for j = starttimeday(i):endtimeday(i)
%         firetot(j) = firetot(j) + firesize(j);
%     end
% end



%%
% filename = 'Temp_final.xlsx';
% temp = xlsread(filename);
% 

load humiddat.mat


hdates = table2array(humid(:,1));
humid = table2array(humid(:,2));

for i = 1:length(humid)
    hdatestr = strsplit(char(hdates(i)), ' ');
    mmm = hdatestr{1};
    year = hdatestr{3};
    dd = hdatestr{2}(1:end-1);
    if(length(dd)<2)
        dd = ['0',dd];
    end
    dnum(i) = datenum([dd, '-', mmm, '-', year]);
end

[shdate, shdateind] = sort(dnum);
shumid = humid(shdateind);
shdate = shdate - shdate(1) + 1;





%%

load u_velocitydat.mat

udates = table2array(u_velocitydat(:,1));
uvar = table2array(u_velocitydat(:,2));

for i = 1:length(uvar)
    udatestr = strsplit(char(udates(i)), ' ');
    mmm = udatestr{1};
    year = udatestr{3};
    dd = udatestr{2}(1:end-1);
    if(length(dd)<2)
        dd = ['0',dd];
    end
    dunum(i) = datenum([dd, '-', mmm, '-', year]);
end

[sudate, sudateind] = sort(dunum);
suvar = uvar(sudateind);
sudate = sudate - sudate(1) + 1;


    
%%
load Vdat.mat


vdates = table2array(Vfinaldat(:,1));
vvar = table2array(Vfinaldat(:,2));

for i = 1:length(vvar)
    vdatestr = char(vdates(i));
    dvnum(i) = datenum(vdates(i));
end

[svdate, svdateind] = sort(dvnum);
svvar = vvar(svdateind);
svdate = svdate - svdate(1) + 1;



%%

load Tempdat.mat

Tdates = table2array(Tempdat(:,1));
Tvar = table2array(Tempdat(:,2));

for i = 1:length(Tvar)
    Tdatestr = char(Tdates(i));
    dTnum(i) = datenum(Tdates(i));
end

[sTdate, sTdateind] = sort(dTnum);
sTvar = Tvar(sTdateind);
sTdate = sTdate - sTdate(1) + 1;


%%

load rainDAT.mat

rdates = table2array(raindat(:,1));
rvar = table2array(raindat(:,2));

for i = 1:length(rvar)
    rdatestr = strsplit(char(rdates(i)), ' ');
    mmm = rdatestr{1};
    year = rdatestr{3};
    dd = rdatestr{2}(1:end-1);
    if(length(dd)<2)
        dd = ['0',dd];
    end
    drnum(i) = datenum([dd, '-', mmm, '-', year]);
end

[srdate, srdateind] = sort(drnum);
srvar = rvar(srdateind);
srdate = srdate - srdate(1) + 1;

%% plots

figure
plot(starttimeday, firesize, '.')

figure
plot(sTdate, sTvar)

figure
plot(svdate, svvar)

figure
plot(sudate, suvar)

figure
plot(shdate, shumid)

figure
plot(srdate, srvar)

A = zeros(length(starttimeday), length(firesize));

% save('output.mat', 'sTdate', 'svdate', 'sudate', 'shdate', 'shumid', 'suvar', 'svvar', 'sTvar', 'starttimeday', 'firesize')

%%%%% ----- %%%%%%

Svvar = [svvar; svvar( length(svvar) - 365: 1817-365-1 )];
Suvar = [suvar; suvar( length(suvar) - 365: 1817-365-1 )];
V = sqrt( Svvar.^2 + Suvar.^2 );
Shumid = [shumid; shumid(1817-365)];
STvar = [sTvar; sTvar( length(sTvar) - 365: 1817-365-1 )];
Srvar = srvar(1:1817);


A = [starttimeday', firesize, Srvar, Shumid, STvar, V];

csvwrite('finalarr.csv', A)

% 
% for i = 1:length(starttimeday)
%     A(i, 1) = starttimeday(i);
%     A(i, 2) = firesize(i);
%     A(i, 3) = 

