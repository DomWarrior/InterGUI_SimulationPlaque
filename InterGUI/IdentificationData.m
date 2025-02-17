function coupe = coupage(nom)
    data2 = readmatrix(nom);
    
    compa = data2(:,2);

    seuil = (((compa(1)-0.09)+(compa(1))+(compa(1)+0.09))/3)+ 0.09; 
    indices = find(compa >= seuil);

    for i = 1:length(indices) - 2
        if indices(i+1) == indices(i) + 1 && indices(i+2) == indices(i) + 2
            indice = indices(i); %
            coupe.incd = indice;
            return;
        end
    end   
end



function couperefroid = coupage2(nom)
    data2 = readmatrix(nom);
    
    compa = data2(:,2);

    seuil = compa(2)- 0.18; 
    indices = find(compa < seuil);

    for i = 1:length(indices) - 2
        if indices(i+1) == indices(i) + 1 && indices(i+2) == indices(i) + 2
            indice = indices(i); 
            couperefroid.incd = indice;
            return;
        end
    end   
end



function dataSet = Usine_DataObject(Nom_du_fichier_CSV, Echelon, freq_echanti, indicerie)
    data = readmatrix(Nom_du_fichier_CSV);
    x = indicerie;

    tempsNonCouper = data(:,1);
    t1noncouper = data(:,2);
    
    dataSet.temps = data(x:end,1);
    dataSet.T1_op = data(x:end,2); 
    dataSet.T2_op = data(x:end,3);
    dataSet.T3_op = data(x:end,4);

    

    
    u_op = Echelon * ones(length(dataSet.temps), 1);

   
    dataSet.U1_T1 = iddata(dataSet.T1_op -  dataSet.T1_op(1), u_op, freq_echanti);
    dataSet.U1_T2 = iddata(dataSet.T2_op - dataSet.T2_op(1), u_op, freq_echanti);
    dataSet.U1_T3 = iddata(dataSet.T3_op - dataSet.T3_op(1), u_op, freq_echanti);
    
    dataSet.T1_T2 = iddata(dataSet.T2_op - dataSet.T2_op(1), dataSet.T1_op -  dataSet.T1_op(1), freq_echanti);
    dataSet.T1_T3 = iddata(dataSet.T3_op - dataSet.T3_op(1), dataSet.T1_op -  dataSet.T1_op(1), freq_echanti);
    dataSet.T2_T3 = iddata(dataSet.T3_op - dataSet.T3_op(1), dataSet.T2_op -  dataSet.T2_op(1), freq_echanti);


    
    plot(tempsNonCouper,t1noncouper)
    hold on 
    plot(dataSet.temps,dataSet.T1_op-dataSet.T1_op(1),"red")
    hold off
end



%Test1 = Usine_DataObject("BONtest2.csv", 1.3455, 0.003,tes1.incd);
%tes1 = coupage("BONtest2.csv");



tes2 = coupage2("BONtest4.csv");
Test2 = Usine_DataObject("BONtest4.csv", -0.64,0.003,tes2.incd);
%disp(tes2.incd)
%systemIdentification