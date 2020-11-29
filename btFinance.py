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


#读取数据库
#初始化数据库
# db_info = {'user': 'root', 'password': 'Peng%Mai_zhf@2014','host': '121.199.15.106','port': 3306,'database': 'Finance'}
# db_info = {'user': 'sa', 'password': 'Talmd13925549389','host': '192.168.1.12','port': 1433,'database': 'TALMD'}
db_info = {'user': 'root', 'password': 'Hdjld^5811%','host': '122.51.235.140','port': 3306,'database': 'Finance'}
engine = create_engine('mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)d/%(database)s?charset=utf8' % db_info, encoding='utf8',connect_args={'charset':'utf8'})

#上市公司股票代码清单
# List=["300668.SZ","300749.SZ","603898.SH","603180.SH","603833.SH","002853.SZ","300616.SZ","002572.SZ","603326.SH","603801.SH","002083.SZ","002327.SZ","002293.SZ","002397.SZ","600337.SH","603818.SH","603389.SH","600978.SH","603816.SH","603313.SH","603008.SH","002489.SZ","603661.SH","603600.SH","603709.SH","000910.SH","002271.SZ","603208.SH","603737.SH","002043.SZ","603515.SH","000541.SZ","002918.SZ","002631.SZ","002718.SZ","002798.SZ","002084.SZ","603385.SH","002722.SZ","300089.SZ","000663.SZ","603038.SH","002818.SZ","601828.SH","002713.SZ","002081.SZ","603030.SH","002482.SZ","601886.SH"
# ]
#%%
# sl=pd.read_excel('X:/02专题分析/上市公司/数据字段列表.xlsx',sheet_name="上市公司列表",index_col=False,error_bad_lines=False,encoding='utf8_general_ci') 
# sl=pd.read_excel('G:/Valuation/汽车/上市公司.xlsx',sheet_name="汽车",index_col=False,error_bad_lines=False,encoding='utf8_general_ci')                                                                                                                         
sl=pd.read_excel('G:/Valuation/上市公司列表.xlsx',index_col=False)                                                                                                                         
SL=sl["股票代码"].values.tolist()

SL1=SL[0:30]
SL2=SL[30:60]
SL3=SL[60:90]
SL4=SL[90:120]
SL5=SL[120:]
                                                                                                                      


#设置token
ts.set_token('632210e8afbd5a1fc1634b019b27df3866dcb8ce7035d7a9d2e39117')

#初始化接口
pro = ts.pro_api(


# %%
class Finance:
    '''
    批量获取上市公司财务数据

    资产负债表（+fields)-pro.balancesheet
    利润表（+fields)-pro.income
    现金流量表（+fields)-pro.cashflow
    主营业务构成（+fields+type)-pro.fina_mainbz
    日线-pro.daily
    月线-pro.monthly
    财务指标-pro.indicator
    偿债能力-ts.get_debtpaying_data
    盈利能力-ts.get_operation_dat
    现金流量-ts.get_cashflow_data
    营运能力-ts.get_profit_data
    业绩报告-ts.get_report_data
    '''
    #主营业务参数
    mb_fields="ts_code,end_date,bz_item,bz_sales,bz_profit,bz_cost,curr_type,update_flag"
    #现金流量表参数
    cf_fields="c_fr_sale_sg,recp_tax_rends,n_depos_incr_fi,n_incr_loans_cb,n_inc_borr_oth_fi,prem_fr_orig_contr,n_incr_insured_dep,n_reinsur_prem,n_incr_disp_tfa,ifc_cash_incr,n_incr_disp_faas,n_incr_loans_oth_bank,n_cap_incr_repur,c_fr_oth_operate_a,c_inf_fr_operate_a,c_paid_goods_s,c_paid_to_for_empl,c_paid_for_taxes,n_incr_clt_loan_adv,n_incr_dep_cbob,c_pay_claims_orig_inco,pay_handling_chrg,pay_comm_insur_plcy,oth_cash_pay_oper_act,st_cash_out_act,n_cashflow_act,oth_recp_ral_inv_act,c_disp_withdrwl_invest,c_recp_return_invest,n_recp_disp_fiolta,n_recp_disp_sobu,c_recp_cap_contrib,incl_cash_rec_saims,uncon_invest_loss,stot_inflows_inv_act,c_pay_acq_const_fiolta,c_paid_invest,n_disp_subs_oth_biz,oth_pay_ral_inv_act,n_incr_pledge_loan,stot_out_inv_act,n_cashflow_inv_act,c_recp_borrow,proc_issue_bonds,oth_cash_recp_ral_fnc_act,stot_cash_in_fnc_act,free_cashflow,c_prepay_amt_borr,c_pay_dist_dpcp_int_exp,incl_dvd_profit_paid_sc_ms,oth_cashpay_ral_fnc_act,stot_cashout_fnc_act,n_cash_flows_fnc_act,eff_fx_flu_cash,n_incr_cash_cash_equ,c_cash_equ_beg_period,c_cash_equ_end_period,net_profit,finan_exp,prov_depr_assets,depr_fa_coga_dpba,amort_intang_assets,lt_amort_deferred_exp,decr_deferred_exp,incr_acc_exp,loss_disp_fiolta,loss_scr_fa,loss_fv_chg,invest_loss,decr_def_inc_tax_assets,incr_def_inc_tax_liab,decr_inventories,decr_oper_payable,incr_oper_payable,others,im_net_cashflow_oper_act,conv_debt_into_cap,conv_copbonds_due_within_1y,fa_fnc_leases,end_bal_cash,beg_bal_cash,end_bal_cash_equ,beg_bal_cash_equ,im_n_incr_cash_equ,ts_code,ann_date,f_ann_date,end_date,update_flag"
    #利润表参数
    is_fields="total_revenue,revenue,int_income,prem_earned,comm_income,n_commis_income,prem_income,out_prem,une_prem_reser,reins_income,n_sec_tb_income,n_sec_uw_income,n_asset_mg_income,oth_b_income,fv_value_chg_gain,invest_income,ass_invest_income,forex_gain,total_cogs,oper_cost,int_exp,comm_exp,biz_tax_surchg,sell_exp,admin_exp,fin_exp,assets_impair_loss,prem_refund,compens_payout,reser_insur_liab,div_payt,reins_exp,oper_exp,compens_payout_refu,insur_reser_refu,reins_cost_refund,other_bus_cost,operate_profit,non_oper_income,non_oper_exp,nca_disploss,total_profit,income_tax,n_income,n_income_attr_p,minority_gain,oth_compr_income,t_compr_income,compr_inc_attr_p,compr_inc_attr_m_s,ebit,ebitda,insurance_exp,undist_profit,distable_profit,basic_eps,diluted_eps,ts_code,ann_date,f_ann_date,end_date,update_flag" 
    #资产负债表参数
    bs_fields="money_cap,sett_rsrv,client_prov,cash_reser_cb,prec_metals,loanto_oth_bank_fi,trad_asset,deriv_assets,notes_receiv,acc_receivable,accounts_receiv,prepayment,amor_exp,premium_receiv,reinsur_receiv,reinsur_res_receiv,rr_reins_une_prem,rr_reins_outstd_cla,int_receiv,div_receiv,oth_receiv,pur_resale_fa,inventories,nca_within_1y,refund_depos,oth_cur_assets,total_cur_assets,ph_pledge_loans,time_deposits,decr_in_disbur,fa_avail_for_sale,htm_invest,lt_rec,lt_eqt_invest,refund_cap_depos,indep_acct_assets,invest_real_estate,fix_assets,cip,const_materials,fixed_assets_disp,produc_bio_assets,oil_and_gas_assets,intan_assets,transac_seat_fee,r_and_d,goodwill,lt_amor_exp,defer_tax_assets,oth_nca,total_nca,oth_assets,total_assets,st_borr,pledge_borr,cb_borr,depos_ib_deposits,loan_oth_bank,trading_fl,deriv_liab,notes_payable,acct_payable,adv_receipts,sold_for_repur_fa,comm_payable,payroll_payable,taxes_payable,int_payable,div_payable,indem_payable,policy_div_payable,ph_invest,rsrv_insur_cont,oth_payable,payable_to_reinsurer,acting_trading_sec,acting_uw_sec,prem_receiv_adva,non_cur_liab_due_1y,oth_cur_liab,total_cur_liab,lt_borr,indept_acc_liab,bond_payable,lt_payable,specific_payables,estimated_liab,defer_tax_liab,oth_ncl,defer_inc_non_cur_liab,total_ncl,oth_liab,total_liab,total_share,oth_eqt_tools,cap_rese,treasury_share,surplus_rese,ordin_risk_reser,undistr_porfit,forex_differ,invest_loss_unconf,special_rese,oth_comp_income,minority_int,total_hldr_eqy_inc_min_int,total_liab_hldr_eqy,ts_code,ann_date,f_ann_date,end_date,update_flag"
    

    def __init__(self,stock_list,start_date,end_date,function,fields,type=""):
        '''
        start_date和end_date的格式为"20201231"
        '''
        self.stock_list=stock_list
        self.start_date=start_date
        self.end_date=end_date 
        self.fields=fields 
        self.function=function
        self.type=type
    

    def get_data(self):
        '''
        获取三大报表数据用法示例（获取现金流量表）：
        cf_=Finance(SL1,"20150101","20201230",pro.cashflow,Finance.cf_fields)
        cf1=Finance.get_data(cf_)
        '''
        data=self.function(ts_code="000000")
        # 调取数据
        for i in range(len(self.stock_list)):
            df=self.function(ts_code=self.stock_list[i],start_date=self.start_date,end_date=self.end_date,fields=self.fields,type=self.type)
            data=data.append(df)
        return data 


    def get_indicator(self):
        '''
        适用于上述ts开头的函数
        '''
        start_year=int(self.start_date[0:4])
        end_year=int(self.end_date[0:4])
        previous_year=start_year-1

        data=self.function(previous_year,4)
        data["quarter"]=str(previous_year)+str(0)+str(4)
        for i in range(start_year,end_year):
            for j in range(1,5):
                df=ts.get_cashflow_data(i,j)
                df["quarter"]=str(i)+str(0)+str(j)
                data=data.append(df)
        return data 


# %%
param_cf=Finance(SL1,"20150101","20201230",pro.cashflow,Finance.cf_fields)
param_is=Finance(SL1,"20150101","20201230",pro.income,Finance.is_fields)
param_bs=Finance(SL1,"20150101","20201230",pro.balancesheet,Finance.bs_fields)
param_mb=Finance(SL1,"20150101","20201230",pro.fina_mainbz,Finance.mb_fields,"p")
cf1=Finance.get_data(param_cf)
is1=Finance.get_data(param_is)
bs1=Finance.get_data(param_bs)
mb1=Finance.get_data(param_mb)
# %%
param_cf=Finance(SL2,"20150101","20201230",pro.cashflow,Finance.cf_fields)
param_is=Finance(SL2,"20150101","20201230",pro.income,Finance.is_fields)
param_bs=Finance(SL2,"20150101","20201230",pro.balancesheet,Finance.bs_fields)
param_mb=Finance(SL2,"20150101","20201230",pro.fina_mainbz,Finance.mb_fields,"p")
cf2=Finance.get_data(param_cf)
is2=Finance.get_data(param_is)
bs2=Finance.get_data(param_bs)
mb2=Finance.get_data(param_mb)
# %%
param_cf=Finance(SL3,"20150101","20201230",pro.cashflow,Finance.cf_fields)
param_is=Finance(SL3,"20150101","20201230",pro.income,Finance.is_fields)
param_bs=Finance(SL3,"20150101","20201230",pro.balancesheet,Finance.bs_fields)
param_mb=Finance(SL3,"20150101","20201230",pro.fina_mainbz,Finance.mb_fields,"p")
cf3=Finance.get_data(param_cf)
is3=Finance.get_data(param_is)
bs3=Finance.get_data(param_bs)
mb3=Finance.get_data(param_mb)
# %%
param_cf=Finance(SL4,"20150101","20201230",pro.cashflow,Finance.cf_fields)
param_is=Finance(SL4,"20150101","20201230",pro.income,Finance.is_fields)
param_bs=Finance(SL4,"20150101","20201230",pro.balancesheet,Finance.bs_fields)
param_mb=Finance(SL4,"20150101","20201230",pro.fina_mainbz,Finance.mb_fields,"p")
cf4=Finance.get_data(param_cf)
is4=Finance.get_data(param_is)
bs4=Finance.get_data(param_bs)
mb4=Finance.get_data(param_mb)
# %%
param_cf=Finance(SL5,"20150101","20201230",pro.cashflow,Finance.cf_fields)
param_is=Finance(SL5,"20150101","20201230",pro.income,Finance.is_fields)
param_bs=Finance(SL5,"20150101","20201230",pro.balancesheet,Finance.bs_fields)
param_mb=Finance(SL5,"20150101","20201230",pro.fina_mainbz,Finance.mb_fields,"p")
cf5=Finance.get_data(param_cf)
is5=Finance.get_data(param_is)
bs5=Finance.get_data(param_bs)
mb5=Finance.get_data(param_mb)