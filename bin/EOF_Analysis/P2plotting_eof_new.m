clear; close all; clc
load ../../Results/all_data;

fileID = fopen('twn_inland.txt','r');
formatSpec = '%f %f'; %defining the format of the data
sizeA = [2 Inf]; %defining the size of the data
A = fscanf(fileID,formatSpec,sizeA); %reading the data using fscanf function
fclose(fileID); %closing the file

data={dN dE dU};
dtnm={'N', 'E', 'U'};
fileID_VE = fopen('../../Results/EOFresults/EOF_modes_VE.txt','w');
for mode=1:2
    close all;
    for dd=1:length(data)
        %For dN
%         size(data{dd})
        [vp, var_porc, eof_p_n, exp_coef_n] = eof_n_optimizado_A2(data{dd});

        
        pcdata=exp_coef_n(:,mode);
        spatialdata=eof_p_n(:,mode);

        save(sprintf('../../Results/EOFresults/pc%d_%s',mode, dtnm{dd}),'tdata','pcdata');
        Adata=[tdata;pcdata'];

        fileID = fopen(sprintf('../../Results/EOFresults/pc%d_%s.txt',mode, dtnm{dd}),'w');
        fprintf(fileID,'%6s %12s\n','tdata','pcdata');
        fprintf(fileID,'%6.2f %12.8f\n',Adata);
        fclose(fileID);
        

        % % %Visualization of the spatial pattern
    %     max(slon)
        xq=min(slon):0.01:122.5;%max(slon);
        yq=min(slat):0.01:max(slat);
        [X,Y]=meshgrid(xq,yq);
        vq = griddata(slon,slat,eof_p_n(:,1),X,Y,'v4');
        F = scatteredInterpolant(slon',slat',eof_p_n(:,mode),'natural','none');
        vq= F(X,Y);
    %     vq_size=size(vq)
        [r,c]=size(vq);

        [in,on] = inpolygon(X,Y,A(1,:),A(2,:)); 
        inon = in | on;                                           
        [rin,cin]=size(inon);

        for i=1:rin
            for j=1:cin
                if (inon(i,j)==0 && inon(i,j)==0)
                    X(i,j)=NaN;
                    Y(i,j)=NaN;
                    vq(i,j)=NaN;
                end
            end 
        end
        Sdata=[slon;slat;spatialdata'];
        fileID = fopen(sprintf('../../Results/EOFresults/spatial%d_%s.txt',mode, dtnm{dd}),'w');
        fprintf(fileID,'%6s %6s %12s\n','lon','lat','spatialEOF');
        fprintf(fileID,'%6.2f %6.2f %12.8f\n',Sdata);
        fclose(fileID);





        %% Using m_map
    %     figure('rend','painters','pos',[100 100 900 600])
        figure()
        m_proj('miller','lat',[21.8,25.5],'lon',[119.5,122.5]);
        
        
%         if mode==1
%             m_pcolor(X,Y,(vq)); shading interp; colormap(flipud(hot));
%             h=colorbar('southoutside');
% 
%             caxis([0.5 1.6])
%         else
%             colorMap1 = [ones(256/4,1),linspace(0,1,256/4)', zeros(256/4,1)];
%             colorMap2 = [ones(256/4,1),ones(256/4,1),linspace(0,1,256/4)'];
%             colorMap3 = [linspace(1,0,256/4)',ones(256/4,1),linspace(1,0,256/4)'];
%             colorMap4 = [zeros(256/4,1),linspace(1,0,256/4)',linspace(0,1,256/4)'];
%             colorMap=[colorMap1; colorMap2; colorMap3; colorMap4];
%             m_pcolor(X,Y,(vq)); shading interp; colormap(flipud(colorMap));
%             h=colorbar('southoutside');
%             maxabsS = max(abs(spatialdata));
% 
%             caxis([-maxabsS maxabsS])
%         end
        colorMap1 = [ones(256/4,1),linspace(0,1,256/4)', zeros(256/4,1)];
        colorMap2 = [ones(256/4,1),ones(256/4,1),linspace(0,1,256/4)'];
        colorMap3 = [linspace(1,0,256/4)',ones(256/4,1),linspace(1,0,256/4)'];
        colorMap4 = [zeros(256/4,1),linspace(1,0,256/4)',linspace(0,1,256/4)'];
        colorMap=[colorMap1; colorMap2; colorMap3; colorMap4];
        m_pcolor(X,Y,(vq)); shading interp; colormap(flipud(colorMap));
        h=colorbar('southoutside');
        if mode==2
            if dtnm{dd}=='N'
                maxabsS = 3;
            elseif dtnm{dd}=='E'
                maxabsS = 2;
            elseif dtnm{dd}=='U'
                maxabsS = 1.5;
            else
                maxabsS = max(abs(spatialdata));
            end
        else
            maxabsS = max(abs(spatialdata));
        end

        caxis([-maxabsS maxabsS])
        hold on
       
        m_line(A(1,:),A(2,:),'color','k','linewi',1);

        for i=1:length(slon)
   
            m_line(slon(i),slat(i),'marker','o','color','k','linewi',1,'linest','none','markersize',4,'markerfacecolor','k');

        end
        
        m_line(120.5928,22.9387,'marker','*','color','red','linewi',1,'linest','none','markersize',10,'markerfacecolor','k');


        m_grid('box','fancy','linestyle','none','fontsize',10,'FontName','Times New Roman','backcolor',[.9 .99 1]);

        title(sprintf('%s',dtnm{dd}))
        fprintf(fileID_VE,'%d %s %.1f\n',mode,dtnm{dd},var_porc(mode));

        ax = gca;
        outerpos = ax.OuterPosition;
        ti = ax.TightInset;
        left = outerpos(1) + ti(1);
        bottom = outerpos(2) + ti(2);
        ax_width = outerpos(3) - ti(2) - ti(3);
        ax_height = outerpos(4) - ti(2) - ti(4);
        ax.Position = [left bottom ax_width ax_height];
        print('-dpng','-r600',[sprintf('../../Results/EOFresults/eof%d_CGPS_comp_spatial',mode), dtnm{dd}]);

    end
end
