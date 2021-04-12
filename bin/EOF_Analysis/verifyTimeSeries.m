clear; close all; clc
load all_filtered_data;

fileID = fopen('twn_inland.txt','r');
formatSpec = '%f %f'; %defining the format of the data
sizeA = [2 Inf]; %defining the size of the data
A = fscanf(fileID,formatSpec,sizeA); %reading the data using fscanf function
fclose(fileID); %closing the file

data={dN -dE dU};

% count=0;
% figure('rend','painters','pos',[100 100 900 600]);
% grid on;
% for i=1:47
%     plot(data{3}(:,i)+count)
%     title(stns(i,:))
%     hold on;
%     count=count+10;
%     fprintf('%d %s %.4f %.4f\n',i,stns(i,:), slon(i), slat(i))
% end
% yticks([0:10:47*10])
% yticklabels(stns)
vlat=22.75;
vlon=120.3;
for i=1:47
    if (slon(i)<vlon+0.1) & (slon(i)>vlon-0.1) & (slat(i)<vlat+0.1) & (slat(i)>vlat-0.1)
        fprintf('%d %s %.4f %.4f\n',i,stns(i,:), slon(i), slat(i))
    end
end

figure
plot(slon,slat,'*')
axis equal;