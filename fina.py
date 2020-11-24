#%%
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 15:18:23 2019

@author: btharp
"""

import tushare as ts
import pandas as pd
import pymysql
import pymssql
from sqlalchemy import create_engine
import os
import requests
from bs4 import BeautifulSoup


#读取数据库
#初始化数据库
# db_info = {'user': 'root', 'password': 'Peng%Mai_zhf@2014','host': '121.199.15.106','port': 3306,'database': 'Finance'}
# db_info = {'user': 'sa', 'password': 'Talmd13925549389','host': '192.168.1.12','port': 1433,'database': 'TALMD'}
#%%

#上市公司股票代码清单
# List=["300668.SZ","300749.SZ","603898.SH","603180.SH","603833.SH","002853.SZ","300616.SZ","002572.SZ","603326.SH","603801.SH","002083.SZ","002327.SZ","002293.SZ","002397.SZ","600337.SH","603818.SH","603389.SH","600978.SH","603816.SH","603313.SH","603008.SH","002489.SZ","603661.SH","603600.SH","603709.SH","000910.SH","002271.SZ","603208.SH","603737.SH","002043.SZ","603515.SH","000541.SZ","002918.SZ","002631.SZ","002718.SZ","002798.SZ","002084.SZ","603385.SH","002722.SZ","300089.SZ","000663.SZ","603038.SH","002818.SZ","601828.SH","002713.SZ","002081.SZ","603030.SH","002482.SZ","601886.SH"
# ]

# sl=pd.read_excel('X:/02专题分析/上市公司/数据字段列表.xlsx',sheet_name="上市公司列表",index_col=False,error_bad_lines=False,encoding='utf8_general_ci') 
# sl=pd.read_excel('G:/Valuation/汽车/上市公司.xlsx',sheet_name="汽车",index_col=False,error_bad_lines=False,encoding='utf8_general_ci')                                                                                                                         
sl=pd.read_excel('G:/Valuation/家居公司/上市公司分析/上市公司列表.xlsx',index_col=False,error_bad_lines=False,encoding='utf8_general_ci')                                                                                                                         
SL=sl["股票代码"].values.tolist()

SL1=SL[0:30]
SL2=SL[30:60]
SL3=SL[60:90]
SL4=SL[90:120]
SL5=SL[120:]
                                                                                                                      


#设置token
ts.set_token('632210e8afbd5a1fc1634b019b27df3866dcb8ce7035d7a9d2e39117')

#初始化接口
pro = ts.pro_api()

#%%
#调取月线数据 
def get_monthly(StockList,start_date,end_date,filename):
    #filename为存储路径和文件名，如："X:/02专题分析/上市公司/上市公司月线.xlsx"
    pe=pro.monthly(ts_code="000000")
    for i in range(len(StockList)):    
        de=pro.monthly(ts_code=StockList[i],start_date=start_date,end_date=end_date)
        pe=pe.append(de)
    #写入excel
    pe.to_excel(filename)
    #写入mysql
    pd.io.sql.to_sql(pe,"Monthly",con=engine, index=False, if_exists='append')
    return pe

#调取日线数据 
def get_daily(StockList,start_date,end_date,filename):
    #filename为存储路径和文件名，如："X:/02专题分析/上市公司/上市公司日线.xlsx"
    pe=pro.daily(ts_code="000000")
    for i in range(len(StockList)):    
        de=pro.daily(ts_code=StockList[i],start_date=start_date,end_date=end_date)
        pe=pe.append(de)
    #写入excel
    pe.to_excel(filename)
    #写入mysql
    #pd.io.sql.to_sql(pe,"Daily",con=engine, index=False, if_exists='append')
    return pe


#%%  三大报表
#调取利润表
def get_income(StockList,start_date,end_date,filename):
    income=pro.income(ts_code="000000")
    fields="total_revenue,revenue,int_income,prem_earned,comm_income,n_commis_income,prem_income,out_prem,une_prem_reser,reins_income,n_sec_tb_income,n_sec_uw_income,n_asset_mg_income,oth_b_income,fv_value_chg_gain,invest_income,ass_invest_income,forex_gain,total_cogs,oper_cost,int_exp,comm_exp,biz_tax_surchg,sell_exp,admin_exp,fin_exp,assets_impair_loss,prem_refund,compens_payout,reser_insur_liab,div_payt,reins_exp,oper_exp,compens_payout_refu,insur_reser_refu,reins_cost_refund,other_bus_cost,operate_profit,non_oper_income,non_oper_exp,nca_disploss,total_profit,income_tax,n_income,n_income_attr_p,minority_gain,oth_compr_income,t_compr_income,compr_inc_attr_p,compr_inc_attr_m_s,ebit,ebitda,insurance_exp,undist_profit,distable_profit,basic_eps,diluted_eps,ts_code,ann_date,f_ann_date,end_date,update_flag"
    #调取数据
    for i in range(len(StockList)):
        ic=pro.income(ts_code=StockList[i],start_date=start_date,end_date=end_date,fields=fields)
        income=income.append(ic)
    #写入excel
    income.to_excel(filename)
    #写入mysql
    # pd.io.sql.to_sql(income,"Income",con=engine, index=False, if_exists='append')
    return income

#调取资产负债表
def get_balancesheet(StockList,start_date,end_date,filename):
    balancesheet=pro.balancesheet(ts_code="000000")
    fields="money_cap,sett_rsrv,client_prov,cash_reser_cb,prec_metals,loanto_oth_bank_fi,trad_asset,deriv_assets,notes_receiv,acc_receivable,accounts_receiv,prepayment,amor_exp,premium_receiv,reinsur_receiv,reinsur_res_receiv,rr_reins_une_prem,rr_reins_outstd_cla,int_receiv,div_receiv,oth_receiv,pur_resale_fa,inventories,nca_within_1y,refund_depos,oth_cur_assets,total_cur_assets,ph_pledge_loans,time_deposits,decr_in_disbur,fa_avail_for_sale,htm_invest,lt_rec,lt_eqt_invest,refund_cap_depos,indep_acct_assets,invest_real_estate,fix_assets,cip,const_materials,fixed_assets_disp,produc_bio_assets,oil_and_gas_assets,intan_assets,transac_seat_fee,r_and_d,goodwill,lt_amor_exp,defer_tax_assets,oth_nca,total_nca,oth_assets,total_assets,st_borr,pledge_borr,cb_borr,depos_ib_deposits,loan_oth_bank,trading_fl,deriv_liab,notes_payable,acct_payable,adv_receipts,sold_for_repur_fa,comm_payable,payroll_payable,taxes_payable,int_payable,div_payable,indem_payable,policy_div_payable,ph_invest,rsrv_insur_cont,oth_payable,payable_to_reinsurer,acting_trading_sec,acting_uw_sec,prem_receiv_adva,non_cur_liab_due_1y,oth_cur_liab,total_cur_liab,lt_borr,indept_acc_liab,bond_payable,lt_payable,specific_payables,estimated_liab,defer_tax_liab,oth_ncl,defer_inc_non_cur_liab,total_ncl,oth_liab,total_liab,total_share,oth_eqt_tools,cap_rese,treasury_share,surplus_rese,ordin_risk_reser,undistr_porfit,forex_differ,invest_loss_unconf,special_rese,oth_comp_income,minority_int,total_hldr_eqy_inc_min_int,total_liab_hldr_eqy,ts_code,ann_date,f_ann_date,end_date,update_flag"
    #调取数据
    for i in range(len(StockList)):
        ic=pro.balancesheet(ts_code=StockList[i],start_date=start_date,end_date=end_date,fields=fields)
        balancesheet=balancesheet.append(ic)
    #写入excel
    balancesheet.to_excel(filename)
    #写入mysql
    #pd.io.sql.to_sql(balancesheet,"BalanceSheet",con=engine, index=False, if_exists='append')
    return balancesheet

#调取现金流量表
def get_cashflow(StockList,start_date,end_date,filename):
    cashflow=pro.cashflow(ts_code="000000")
    fields="c_fr_sale_sg,recp_tax_rends,n_depos_incr_fi,n_incr_loans_cb,n_inc_borr_oth_fi,prem_fr_orig_contr,n_incr_insured_dep,n_reinsur_prem,n_incr_disp_tfa,ifc_cash_incr,n_incr_disp_faas,n_incr_loans_oth_bank,n_cap_incr_repur,c_fr_oth_operate_a,c_inf_fr_operate_a,c_paid_goods_s,c_paid_to_for_empl,c_paid_for_taxes,n_incr_clt_loan_adv,n_incr_dep_cbob,c_pay_claims_orig_inco,pay_handling_chrg,pay_comm_insur_plcy,oth_cash_pay_oper_act,st_cash_out_act,n_cashflow_act,oth_recp_ral_inv_act,c_disp_withdrwl_invest,c_recp_return_invest,n_recp_disp_fiolta,n_recp_disp_sobu,c_recp_cap_contrib,incl_cash_rec_saims,uncon_invest_loss,stot_inflows_inv_act,c_pay_acq_const_fiolta,c_paid_invest,n_disp_subs_oth_biz,oth_pay_ral_inv_act,n_incr_pledge_loan,stot_out_inv_act,n_cashflow_inv_act,c_recp_borrow,proc_issue_bonds,oth_cash_recp_ral_fnc_act,stot_cash_in_fnc_act,free_cashflow,c_prepay_amt_borr,c_pay_dist_dpcp_int_exp,incl_dvd_profit_paid_sc_ms,oth_cashpay_ral_fnc_act,stot_cashout_fnc_act,n_cash_flows_fnc_act,eff_fx_flu_cash,n_incr_cash_cash_equ,c_cash_equ_beg_period,c_cash_equ_end_period,net_profit,finan_exp,prov_depr_assets,depr_fa_coga_dpba,amort_intang_assets,lt_amort_deferred_exp,decr_deferred_exp,incr_acc_exp,loss_disp_fiolta,loss_scr_fa,loss_fv_chg,invest_loss,decr_def_inc_tax_assets,incr_def_inc_tax_liab,decr_inventories,decr_oper_payable,incr_oper_payable,others,im_net_cashflow_oper_act,conv_debt_into_cap,conv_copbonds_due_within_1y,fa_fnc_leases,end_bal_cash,beg_bal_cash,end_bal_cash_equ,beg_bal_cash_equ,im_n_incr_cash_equ,ts_code,ann_date,f_ann_date,end_date,update_flag"
    #调取数据
    for i in range(len(StockList)):
        ic=pro.cashflow(ts_code=StockList[i],start_date=start_date,end_date=end_date,fields=fields)
        cashflow=cashflow.append(ic)
    #写入excel
    cashflow.to_excel(filename)
    #写入mysql
    #pd.io.sql.to_sql(cashflow,"CashFlow",con=engine, index=False, if_exists='append')
    return cashflow


# %% 调取主营业务
def get_main(StockList,start_date,end_date,filename,type):
    mainbz=pro.fina_mainbz(ts_code="000000")
    mbf="ts_code,end_date,bz_item,bz_sales,bz_profit,bz_cost,curr_type,update_flag"
    #调取数据
    for i in range(len(StockList)):
        ic=pro.fina_mainbz(ts_code=StockList[i],start_date=start_date,end_date=end_date,fields=mbf,type=type)
        mainbz=mainbz.append(ic)
    #写入excel
    mainbz.to_excel(filename)
    #写入mysql
    #pd.io.sql.to_sql(cashflow,"CashFlow",con=engine, index=False, if_exists='append')
    return mainbz

def report(FileName):
    # "X:/02专题分析/上市公司/上市公司业绩报告.xlsx"
    report=ts.get_report_data(2015,4)
    for i in range(2016,2021):
        for j in range(1,5):
            df=ts.get_report_data(i,j)
            df["quarter"]=str(i)+str(0)+str(j)
            report=report.append(df)
    report.to_excel(FileName)
    return report


#%%  财务指标
def get_fina(StockList,start_date,end_date,filename):
#创建空白dataframe
    fina=pro.fina_indicator(ts_code="000000")
#日期的格式为"20190631"
    #调取数据
    for i in range(len(StockList)):
        df=pro.fina_indicator(ts_code=StockList[i],start_date=start_date,end_date=end_date)
        fina=fina.append(df)
    #写入excel
    fina.to_excel(filename)
    #写入mysql
    pd.io.sql.to_sql(fina,"Indicators",con=engine, index=False, if_exists='append')
    return fina

#盈利能力            
def profit(filename):
    profit=ts.get_profit_data(2015,4)
    profit["quarter"]="201504"
    for i in range(2016,2021):
        for j in range(1,5):
            df=ts.get_profit_data(i,j)
            df["quarter"]=str(i)+str(0)+str(j)
            profit=profit.append(df)
    profit.to_excel(filename)
    return profit

#营运能力            
def operation(filename):
    d=ts.get_operation_data(2015,4)
    d["quarter"]="201504"
    for i in range(2016,2021):
        for j in range(1,5):
            df=ts.get_operation_data(i,j)
            df["quarter"]=str(i)+str(0)+str(j)
            d=d.append(df)
    d.to_excel(filename)
    return d

#成长能力            
def growth(filename):
    d=ts.get_growth_data(2015,4)
    d["quarter"]="201504"
    for i in range(2016,2021):
        for j in range(1,5):
            df=ts.get_growth_data(i,j)
            df["quarter"]=str(i)+str(0)+str(j)
            d=d.append(df)
    d.to_excel(filename)
    return d

#偿债能力            
def debtpaying(filename):
    d=ts.get_debtpaying_data(2015,4)
    d["quarter"]="201504"
    for i in range(2016,2021):
        for j in range(1,5):
            df=ts.get_debtpaying_data(i,j)
            df["quarter"]=str(i)+str(0)+str(j)
            d=d.append(df)
    d.to_excel(filename)
    return d

#现金流量            
def cashflow(filename):
    d=ts.get_cashflow_data(2015,4)
    d["quarter"]="201504"
    for i in range(2016,2021):
        for j in range(1,5):
            df=ts.get_cashflow_data(i,j)
            df["quarter"]=str(i)+str(0)+str(j)
            d=d.append(df)
    d.to_excel(filename)
    return d


# %%  爬取新浪财经的各公司研报，取前10页
def research_report(StockList):
    report=pd.DataFrame()
    for i in range(len(StockList)):
        try:
            PreUrl="http://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?t1=2&symbol="
            StockCode=StockList[i][0:6]
            r=pd.DataFrame()
            for j in range(10):  # 页数
                try:
                    res = requests.get(PreUrl+StockCode+"&p="+str(j)) #模拟get请求获取链接返回的内容
                    # res.encoding = 'utf-8'#设置编码格式为utf-8
                    soup = BeautifulSoup(res.text, 'html.parser')#前面已经介绍将html文档格式化为一个树形结构，每个节点都是一个对python对象，方便获取节点内容        
        
                    table=soup.select(".main")[0].find_all("table")[0] # 解析为上下两个表，上表为研报数据，下表为页码
                    trList=table.find_all("tr")  # 解析为每行记录的列表

                    href=[]
                    title=[]
                    date=[]
                    company=[]
                    author=[]

                    for k in range(2,len(trList)):  #前两行为表头
                        tr=trList[k]
                        href.append(tr.find("a")["href"])
                        title.append(tr.find("a")["title"])
                        tdList=tr.find_all("td")
                        # 第一个td是行号，
                        # 第二个td是文章标题和链接，
                        # 第三个td是类型，这里都是公司
                        # 第四个td是日期
                        # 第五个td是本页链接及研报公司名称
                        # 第六个td是作者
                        date.append(tdList[3].get_text())
                        company.append(tdList[4].find("span").get_text())
                        author.append(tdList[5].find("span").get_text())


                    rp=pd.DataFrame({"href":href,"title":title,"date":date,"company":company,"author":author})
                    rp["Stock"]=StockList[i]
                    r=r.append(rp)
                except:
                    pass
            report=report.append(r)
        except:
            pass
    return report 



# %%
report
# %%
rep=research_report(StockList)
# %%
rep.shape
# %%
rep.tail()
# %%
pd.io.sql.to_sql(rep,"Reports",con=engine, index=False, if_exists='replace')
# %%
