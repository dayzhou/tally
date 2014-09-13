<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<!-- <link href="tally.css" rel=stylesheet type=text/css> -->
<title>Tally</title>

<style type="text/css">
% include( 'tally.css' )
</style>

</head>
<body>

<div class="left">
    <div class="left_box">
        <p><a href="/record">记账啦</a></p>
        <p><a href="/view">查水表</a></p>
    </div>
</div>

<div class="right">

% if operation == 'RECORD' :
    <div class="right_box">
    <p>在下面写上你的花销吧</p>
    <div style="border-bottom: 1px solid #3399FF; width: 300px;"></div>
    
    <form method=post action="/record">
        <table cellspacing=5 style="margin-top:10px; margin-bottom: 10px; border: 0px solid #3399FF;">
    % for i,row in enumerate( InputRows ) :
        <tr>
            <td></td>
            <td><font color=red>{{row.msg['ware']}}</font></td>
            
            <td></td>
            <td><font color=red>{{row.msg['cost']}}</font></td>
            
            <td></td>
            <td><font color=red>{{row.msg['remark']}}</font></td>
            
            <td></td>
            <td><font color=red>{{row.msg['date']}}</font></td>
        </tr>
        <tr>
            <td>商品</td>
            <td><input type=text name=ware{{i}} size=25 value='{{row.ware}}'></td>
            
            <td> &nbsp; 金额</td>
            <td><select name=currency{{i}}>
        % for c in AllCurrencies :
                <option value={{c.curid}} {{'selected' if c.curid==row.currency else ''}}>{{!c.html}}
        % end
                </select>
                <input type=text name=cost{{i}} size=10 value='{{row.cost}}'>
            </td>
            
            <td> &nbsp; 备注</td>
            <td><input type=text name=remark{{i}} size=30 value='{{row.remark}}'></td>
            
        % year, month, day = row.date.split('-')
            <td> &nbsp; 日期</td>
            <td><input type=text name=year{{i}} size=4 value='{{year}}'> -
                <input type=text name=month{{i}} size=2 value='{{month}}'> -
                <input type=text name=day{{i}} size=2 value='{{day}}'>
            </td>
        </tr>
    % end
        </table>
        <input class="LoginButton" type=submit value=提交>
    </form>
    </div>
% end


% if operation == 'VIEW' :
    <div class="right_box">
    <form method=post action="/view">
        <table style="margin-top:10px; margin-bottom: 10px; border: 0px solid #3399FF;">
        <tr>
        <td width=100>选择年月</td>
        <td width=200><select name=year>
        % for y in AllYears :
            <option {{'selected' if y==year else ''}}>{{y}}
        % end
            </select>
            <select name=month>
        % for m in [ '%02d' % mo for mo in range(1,13) ] :
            <option {{'selected' if m==month else ''}}>{{m}}
        % end
            </select>
        </td>
        <td><input class="LoginButton" type=submit value=查询>
        </tr>
        </table>
    </form>
    
    <div style="border-bottom: 1px solid #3399FF; width: 400px;"></div>
    
    <table class="table_border" style="margin-top:20px;">
        <tr align=center>
            <td width=100>日期</td>
            <td width=200>商品</td>
            <td width=120>金额</td>
            <td width=200>备忘</td>
        </tr>
        % for row in TallyRows :
            <tr align=center>
            <td width=100>{{row.date}}</td>
            <td width=200>{{row.ware}}</td>
            <td width=120>{{!row.cost}}</td>
            <td width=200>{{row.remark}}</td>
            </tr>
        % end
        <tr><td colspan=4></td></tr>
        % for row in TotalTallyRows :
            <tr align=center>
            <td width=100><font color=green>Total</font></td>
            <td width=200>-</td>
            <td width=120><font color=green>{{!row.cost}}</font></td>
            <td width=200>-</td>
            </tr>
        % end
    </table>
    </div>
% end

</div>
</body>