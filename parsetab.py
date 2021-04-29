
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ADD AND CAPT CB CHAR CLASS CLASS_ID COL COMMA CP CSB CTE_CHAR CTE_F CTE_I CTE_STRING DATAFRAME DIGIT DIGITS DIV ELSE EQ EQEQ FILE FLOAT FOR GE GT ID IF INT LE LETTER LT MULT NE OB OP OR OSB POINT PROGRAM SC SUB VOID WHILEprograma : PROGRAM ID SC programa_a bloqueprograma_a : programa_b\n                | programa_b programa_a\n                | emptyprograma_b : vars\n                | vars_vect_matvars : tiposimple vars_a SC\n            | tipocompuesto vars_a SCvars_a : vars_b\n            | vars_b COMMA vars_avars_b : ID\n            | ID EQ expresionvars_vect_mat : tiposimple ID vars_vect_mat_a SC\n                    | tiposimple ID vars_vect_mat_a vars_vect_mat_a SCvars_vect_mat_a : OSB exp CSBm_exp : m_exp_b\n            | m_exp_b m_exp_a m_expm_exp_a : ADD\n            | SUBm_exp_b : term term : term_b\n            | term_b term_a termterm_a : MULT\n            | DIVterm_b : facttiposimple : INT\n                | FLOAT\n                | CHARtipocompuesto : DATAFRAME\n                    | ID\n                    | FILEbloque : OB bloque_a CBbloque_a : estatuto bloque_a\n                | estatuto\n                | emptyestatuto : asignacion\n                | condicion\n                | llamada\n                | while\n                | for\n                | classcreate\n                | vars\n                | classdeclare\n                | llamadafuncionclase\n                | functionexpresion : m_exp\n                | m_exp expresion_a m_expexpresion_a : LT\n                | GT\n                | NE\n                | EQEQ\n                | LE\n                | GEvarcte : ID\n            | CTE_I\n            | CTE_Fwhile : while_b bloquewhile_a : WHILEwhile_b : while_a OP expresion CPexp : and_exp exp_aexp_a : OR\n            | emptyand_exp : expresion and_exp_aand_exp_a : AND\n                | emptyfor : FOR OP asignacionsencilla SC expresion SC asignacionsencilla CP bloquellamada : ID OP llamada_a CP SCllamada_a : expresion llamada_b\n                | CTE_STRING llamada_b\n                | llamada_bllamada_b : COMMA llamada_a\n                | emptyfact : fact_a exp CP\n            | CTE_I\n            | CTE_F\n            | CTE_CHAR\n            | ID\n            | llamadafact_a : OPclasscreate : CLASS CLASS_ID OB classcreate_a function classcreate_c CBclasscreate_a : vars classcreate_a\n                    | vars_vect_mat classcreate_a\n                    | emptyclasscreate_c : function classcreate_d\n                    | classcreate_dclasscreate_d : classcreate_c\n                    | emptycondicion : IF OP expresion CP bloque condicion_acondicion_a : ELSE condicion_b bloquecondicion_b : condicion\n                | emptyclassdeclare : CLASS_ID ID SCllamadafuncionclase : ID POINT llamadaasignacion : ID asignacion_a asignacion_a EQ expresion SCasignacion_a : OSB exp CSB\n                    | emptyasignacionsencilla : ID EQ expresionfunction : function_a ID OP function_b CP bloquefunction_a : VOID\n                | tiposimplefunction_b : tiposimple ID\n                | tiposimple ID COMMA function_b\n                | emptyempty :'
    
_lr_action_items = {'PROGRAM':([0,],[2,]),'$end':([1,18,56,],[0,-1,-32,]),'ID':([2,4,5,7,9,10,11,12,13,14,15,16,17,19,27,29,30,31,32,33,34,35,36,37,38,39,44,45,46,48,50,52,53,54,55,56,59,60,61,63,64,65,69,71,79,84,94,97,102,103,106,107,108,109,110,111,112,113,114,115,116,117,118,119,128,135,136,138,139,142,150,155,160,161,163,168,176,178,180,],[3,5,-30,5,-5,-6,22,25,-26,-27,-28,-29,-31,39,39,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-30,67,25,68,-99,-7,72,72,25,-8,-32,72,96,72,72,-57,101,72,-13,72,-79,72,-93,5,-92,-14,72,-48,-49,-50,-51,-52,-53,72,-18,-19,72,-23,-24,72,72,72,5,5,159,-67,-100,-94,-88,101,-98,-80,-89,-66,]),'SC':([3,21,22,23,24,25,51,67,70,72,73,74,75,76,77,78,80,81,82,83,88,100,121,129,145,146,147,148,149,150,152,153,],[4,50,-11,-9,55,-11,71,103,106,-77,-12,-46,-16,-20,-21,-25,-74,-75,-76,-78,-10,135,-15,150,-47,-17,-22,-73,160,-67,163,-97,]),'OB':([4,6,7,8,9,10,20,41,50,55,56,66,71,106,134,144,158,161,162,170,171,172,178,179,],[-104,19,-2,-4,-5,-6,-3,19,-7,-8,-32,102,-13,-14,19,-59,19,-88,-104,19,-90,-91,-89,19,]),'INT':([4,7,9,10,19,27,29,30,31,32,33,34,35,36,37,38,50,55,56,64,71,97,102,103,104,106,137,138,139,140,150,154,156,157,160,161,164,168,169,176,178,180,],[13,13,-5,-6,13,13,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-7,-8,-32,-57,-13,-93,13,-92,13,-14,13,13,13,-83,-67,13,-81,-82,-94,-88,13,-98,13,-80,-89,-66,]),'FLOAT':([4,7,9,10,19,27,29,30,31,32,33,34,35,36,37,38,50,55,56,64,71,97,102,103,104,106,137,138,139,140,150,154,156,157,160,161,164,168,169,176,178,180,],[14,14,-5,-6,14,14,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-7,-8,-32,-57,-13,-93,14,-92,14,-14,14,14,14,-83,-67,14,-81,-82,-94,-88,14,-98,14,-80,-89,-66,]),'CHAR':([4,7,9,10,19,27,29,30,31,32,33,34,35,36,37,38,50,55,56,64,71,97,102,103,104,106,137,138,139,140,150,154,156,157,160,161,164,168,169,176,178,180,],[15,15,-5,-6,15,15,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-7,-8,-32,-57,-13,-93,15,-92,15,-14,15,15,15,-83,-67,15,-81,-82,-94,-88,15,-98,15,-80,-89,-66,]),'DATAFRAME':([4,7,9,10,19,27,29,30,31,32,33,34,35,36,37,38,50,55,56,64,71,97,102,103,106,138,139,150,160,161,168,176,178,180,],[16,16,-5,-6,16,16,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-7,-8,-32,-57,-13,-93,16,-92,-14,16,16,-67,-94,-88,-98,-80,-89,-66,]),'FILE':([4,7,9,10,19,27,29,30,31,32,33,34,35,36,37,38,50,55,56,64,71,97,102,103,106,138,139,150,160,161,168,176,178,180,],[17,17,-5,-6,17,17,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-7,-8,-32,-57,-13,-93,17,-92,-14,17,17,-67,-94,-88,-98,-80,-89,-66,]),'CB':([19,26,27,28,29,30,31,32,33,34,35,36,37,38,50,55,56,57,64,97,103,150,154,160,161,164,165,166,167,168,174,175,176,178,180,],[-104,56,-34,-35,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-7,-8,-32,-33,-57,-93,-92,-67,-104,-94,-88,-104,176,-85,-87,-98,-84,-86,-80,-89,-66,]),'IF':([19,27,29,30,31,32,33,34,35,36,37,38,50,55,56,64,97,103,150,160,161,162,168,176,178,180,],[40,40,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-7,-8,-32,-57,-93,-92,-67,-94,-88,40,-98,-80,-89,-66,]),'FOR':([19,27,29,30,31,32,33,34,35,36,37,38,50,55,56,64,97,103,150,160,161,168,176,178,180,],[42,42,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-7,-8,-32,-57,-93,-92,-67,-94,-88,-98,-80,-89,-66,]),'CLASS':([19,27,29,30,31,32,33,34,35,36,37,38,50,55,56,64,97,103,150,160,161,168,176,178,180,],[43,43,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-7,-8,-32,-57,-93,-92,-67,-94,-88,-98,-80,-89,-66,]),'CLASS_ID':([19,27,29,30,31,32,33,34,35,36,37,38,43,50,55,56,64,97,103,150,160,161,168,176,178,180,],[44,44,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,66,-7,-8,-32,-57,-93,-92,-67,-94,-88,-98,-80,-89,-66,]),'VOID':([19,27,29,30,31,32,33,34,35,36,37,38,50,55,56,64,71,97,102,103,106,137,138,139,140,150,154,156,157,160,161,164,168,176,178,180,],[48,48,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-7,-8,-32,-57,-13,-93,-104,-92,-14,48,-104,-104,-83,-67,48,-81,-82,-94,-88,48,-98,-80,-89,-66,]),'WHILE':([19,27,29,30,31,32,33,34,35,36,37,38,50,55,56,64,97,103,150,160,161,168,176,178,180,],[49,49,-36,-37,-38,-39,-40,-41,-42,-43,-44,-45,-7,-8,-32,-57,-93,-92,-67,-94,-88,-98,-80,-89,-66,]),'COMMA':([22,23,25,59,72,73,74,75,76,77,78,80,81,82,83,91,93,94,145,146,147,148,150,159,],[-11,54,-11,94,-77,-12,-46,-16,-20,-21,-25,-74,-75,-76,-78,94,94,94,-47,-17,-22,-73,-67,169,]),'EQ':([22,25,39,58,62,89,101,133,],[52,52,-104,-104,-96,128,136,-95,]),'OSB':([22,39,51,58,62,121,133,],[53,61,53,61,-96,-15,-95,]),'OP':([39,40,42,47,49,52,53,59,61,63,68,69,72,79,84,94,96,107,108,109,110,111,112,113,114,115,116,117,118,119,128,135,136,],[59,63,65,69,-58,84,84,84,84,84,104,84,59,84,-79,84,59,84,-48,-49,-50,-51,-52,-53,84,-18,-19,84,-23,-24,84,84,84,]),'POINT':([39,],[60,]),'CTE_I':([52,53,59,61,63,69,79,84,94,107,108,109,110,111,112,113,114,115,116,117,118,119,128,135,136,],[80,80,80,80,80,80,80,-79,80,80,-48,-49,-50,-51,-52,-53,80,-18,-19,80,-23,-24,80,80,80,]),'CTE_F':([52,53,59,61,63,69,79,84,94,107,108,109,110,111,112,113,114,115,116,117,118,119,128,135,136,],[81,81,81,81,81,81,81,-79,81,81,-48,-49,-50,-51,-52,-53,81,-18,-19,81,-23,-24,81,81,81,]),'CTE_CHAR':([52,53,59,61,63,69,79,84,94,107,108,109,110,111,112,113,114,115,116,117,118,119,128,135,136,],[82,82,82,82,82,82,82,-79,82,82,-48,-49,-50,-51,-52,-53,82,-18,-19,82,-23,-24,82,82,82,]),'ELSE':([56,151,],[-32,162,]),'CTE_STRING':([59,94,],[93,93,]),'CP':([59,72,74,75,76,77,78,80,81,82,83,86,87,90,91,92,93,94,95,99,104,105,120,122,123,124,125,126,127,130,131,132,141,143,145,146,147,148,150,153,159,169,173,177,],[-104,-77,-46,-16,-20,-21,-25,-74,-75,-76,-78,-104,-104,129,-104,-70,-104,-104,-72,134,-104,144,148,-60,-61,-62,-63,-64,-65,-68,-69,-71,158,-103,-47,-17,-22,-73,-67,-97,-101,-104,179,-102,]),'MULT':([72,77,78,80,81,82,83,148,150,],[-77,118,-25,-74,-75,-76,-78,-73,-67,]),'DIV':([72,77,78,80,81,82,83,148,150,],[-77,119,-25,-74,-75,-76,-78,-73,-67,]),'ADD':([72,75,76,77,78,80,81,82,83,147,148,150,],[-77,115,-20,-21,-25,-74,-75,-76,-78,-22,-73,-67,]),'SUB':([72,75,76,77,78,80,81,82,83,147,148,150,],[-77,116,-20,-21,-25,-74,-75,-76,-78,-22,-73,-67,]),'LT':([72,74,75,76,77,78,80,81,82,83,146,147,148,150,],[-77,108,-16,-20,-21,-25,-74,-75,-76,-78,-17,-22,-73,-67,]),'GT':([72,74,75,76,77,78,80,81,82,83,146,147,148,150,],[-77,109,-16,-20,-21,-25,-74,-75,-76,-78,-17,-22,-73,-67,]),'NE':([72,74,75,76,77,78,80,81,82,83,146,147,148,150,],[-77,110,-16,-20,-21,-25,-74,-75,-76,-78,-17,-22,-73,-67,]),'EQEQ':([72,74,75,76,77,78,80,81,82,83,146,147,148,150,],[-77,111,-16,-20,-21,-25,-74,-75,-76,-78,-17,-22,-73,-67,]),'LE':([72,74,75,76,77,78,80,81,82,83,146,147,148,150,],[-77,112,-16,-20,-21,-25,-74,-75,-76,-78,-17,-22,-73,-67,]),'GE':([72,74,75,76,77,78,80,81,82,83,146,147,148,150,],[-77,113,-16,-20,-21,-25,-74,-75,-76,-78,-17,-22,-73,-67,]),'AND':([72,74,75,76,77,78,80,81,82,83,87,145,146,147,148,150,],[-77,-46,-16,-20,-21,-25,-74,-75,-76,-78,126,-47,-17,-22,-73,-67,]),'OR':([72,74,75,76,77,78,80,81,82,83,86,87,125,126,127,145,146,147,148,150,],[-77,-46,-16,-20,-21,-25,-74,-75,-76,-78,123,-104,-63,-64,-65,-47,-17,-22,-73,-67,]),'CSB':([72,74,75,76,77,78,80,81,82,83,85,86,87,98,122,123,124,125,126,127,145,146,147,148,150,],[-77,-46,-16,-20,-21,-25,-74,-75,-76,-78,121,-104,-104,133,-60,-61,-62,-63,-64,-65,-47,-17,-22,-73,-67,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'programa':([0,],[1,]),'programa_a':([4,7,],[6,20,]),'programa_b':([4,7,],[7,7,]),'empty':([4,7,19,27,39,58,59,86,87,91,93,94,102,104,138,139,154,162,164,169,],[8,8,28,28,62,62,95,124,127,95,95,95,140,143,140,140,167,172,167,143,]),'vars':([4,7,19,27,102,138,139,],[9,9,35,35,138,138,138,]),'vars_vect_mat':([4,7,102,138,139,],[10,10,139,139,139,]),'tiposimple':([4,7,19,27,102,104,137,138,139,154,164,169,],[11,11,45,45,11,142,155,11,11,155,155,142,]),'tipocompuesto':([4,7,19,27,102,138,139,],[12,12,12,12,12,12,12,]),'bloque':([6,41,134,158,170,179,],[18,64,151,168,178,180,]),'vars_a':([11,12,45,54,],[21,24,21,88,]),'vars_b':([11,12,45,54,],[23,23,23,23,]),'bloque_a':([19,27,],[26,57,]),'estatuto':([19,27,],[27,27,]),'asignacion':([19,27,],[29,29,]),'condicion':([19,27,162,],[30,30,171,]),'llamada':([19,27,52,53,59,60,61,63,69,79,94,107,114,117,128,135,136,],[31,31,83,83,83,97,83,83,83,83,83,83,83,83,83,83,83,]),'while':([19,27,],[32,32,]),'for':([19,27,],[33,33,]),'classcreate':([19,27,],[34,34,]),'classdeclare':([19,27,],[36,36,]),'llamadafuncionclase':([19,27,],[37,37,]),'function':([19,27,137,154,164,],[38,38,154,164,164,]),'while_b':([19,27,],[41,41,]),'function_a':([19,27,137,154,164,],[46,46,46,46,46,]),'while_a':([19,27,],[47,47,]),'vars_vect_mat_a':([22,51,],[51,70,]),'asignacion_a':([39,58,],[58,89,]),'expresion':([52,53,59,61,63,69,79,94,128,135,136,],[73,87,91,87,99,105,87,91,149,152,153,]),'m_exp':([52,53,59,61,63,69,79,94,107,114,128,135,136,],[74,74,74,74,74,74,74,74,145,146,74,74,74,]),'m_exp_b':([52,53,59,61,63,69,79,94,107,114,128,135,136,],[75,75,75,75,75,75,75,75,75,75,75,75,75,]),'term':([52,53,59,61,63,69,79,94,107,114,117,128,135,136,],[76,76,76,76,76,76,76,76,76,76,147,76,76,76,]),'term_b':([52,53,59,61,63,69,79,94,107,114,117,128,135,136,],[77,77,77,77,77,77,77,77,77,77,77,77,77,77,]),'fact':([52,53,59,61,63,69,79,94,107,114,117,128,135,136,],[78,78,78,78,78,78,78,78,78,78,78,78,78,78,]),'fact_a':([52,53,59,61,63,69,79,94,107,114,117,128,135,136,],[79,79,79,79,79,79,79,79,79,79,79,79,79,79,]),'exp':([53,61,79,],[85,98,120,]),'and_exp':([53,61,79,],[86,86,86,]),'llamada_a':([59,94,],[90,132,]),'llamada_b':([59,91,93,94,],[92,130,131,92,]),'asignacionsencilla':([65,163,],[100,173,]),'expresion_a':([74,],[107,]),'m_exp_a':([75,],[114,]),'term_a':([77,],[117,]),'exp_a':([86,],[122,]),'and_exp_a':([87,],[125,]),'classcreate_a':([102,138,139,],[137,156,157,]),'function_b':([104,169,],[141,177,]),'condicion_a':([151,],[161,]),'classcreate_c':([154,164,],[165,175,]),'classcreate_d':([154,164,],[166,174,]),'condicion_b':([162,],[170,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> programa","S'",1,None,None,None),
  ('programa -> PROGRAM ID SC programa_a bloque','programa',5,'p_programa','ScannerParser.py',428),
  ('programa_a -> programa_b','programa_a',1,'p_programa_a','ScannerParser.py',432),
  ('programa_a -> programa_b programa_a','programa_a',2,'p_programa_a','ScannerParser.py',433),
  ('programa_a -> empty','programa_a',1,'p_programa_a','ScannerParser.py',434),
  ('programa_b -> vars','programa_b',1,'p_programa_b','ScannerParser.py',438),
  ('programa_b -> vars_vect_mat','programa_b',1,'p_programa_b','ScannerParser.py',439),
  ('vars -> tiposimple vars_a SC','vars',3,'p_vars','ScannerParser.py',443),
  ('vars -> tipocompuesto vars_a SC','vars',3,'p_vars','ScannerParser.py',444),
  ('vars_a -> vars_b','vars_a',1,'p_vars_a','ScannerParser.py',455),
  ('vars_a -> vars_b COMMA vars_a','vars_a',3,'p_vars_a','ScannerParser.py',456),
  ('vars_b -> ID','vars_b',1,'p_vars_b','ScannerParser.py',459),
  ('vars_b -> ID EQ expresion','vars_b',3,'p_vars_b','ScannerParser.py',460),
  ('vars_vect_mat -> tiposimple ID vars_vect_mat_a SC','vars_vect_mat',4,'p_vars_vect_mat','ScannerParser.py',472),
  ('vars_vect_mat -> tiposimple ID vars_vect_mat_a vars_vect_mat_a SC','vars_vect_mat',5,'p_vars_vect_mat','ScannerParser.py',473),
  ('vars_vect_mat_a -> OSB exp CSB','vars_vect_mat_a',3,'p_vars_vect_mat_a','ScannerParser.py',477),
  ('m_exp -> m_exp_b','m_exp',1,'p_m_exp','ScannerParser.py',481),
  ('m_exp -> m_exp_b m_exp_a m_exp','m_exp',3,'p_m_exp','ScannerParser.py',482),
  ('m_exp_a -> ADD','m_exp_a',1,'p_m_exp_a','ScannerParser.py',486),
  ('m_exp_a -> SUB','m_exp_a',1,'p_m_exp_a','ScannerParser.py',487),
  ('m_exp_b -> term','m_exp_b',1,'p_m_exp_b','ScannerParser.py',493),
  ('term -> term_b','term',1,'p_term','ScannerParser.py',498),
  ('term -> term_b term_a term','term',3,'p_term','ScannerParser.py',499),
  ('term_a -> MULT','term_a',1,'p_term_a','ScannerParser.py',503),
  ('term_a -> DIV','term_a',1,'p_term_a','ScannerParser.py',504),
  ('term_b -> fact','term_b',1,'p_term_b','ScannerParser.py',510),
  ('tiposimple -> INT','tiposimple',1,'p_tiposimple','ScannerParser.py',515),
  ('tiposimple -> FLOAT','tiposimple',1,'p_tiposimple','ScannerParser.py',516),
  ('tiposimple -> CHAR','tiposimple',1,'p_tiposimple','ScannerParser.py',517),
  ('tipocompuesto -> DATAFRAME','tipocompuesto',1,'p_tipocompuesto','ScannerParser.py',522),
  ('tipocompuesto -> ID','tipocompuesto',1,'p_tipocompuesto','ScannerParser.py',523),
  ('tipocompuesto -> FILE','tipocompuesto',1,'p_tipocompuesto','ScannerParser.py',524),
  ('bloque -> OB bloque_a CB','bloque',3,'p_bloque','ScannerParser.py',528),
  ('bloque_a -> estatuto bloque_a','bloque_a',2,'p_bloque_a','ScannerParser.py',532),
  ('bloque_a -> estatuto','bloque_a',1,'p_bloque_a','ScannerParser.py',533),
  ('bloque_a -> empty','bloque_a',1,'p_bloque_a','ScannerParser.py',534),
  ('estatuto -> asignacion','estatuto',1,'p_estatuto','ScannerParser.py',538),
  ('estatuto -> condicion','estatuto',1,'p_estatuto','ScannerParser.py',539),
  ('estatuto -> llamada','estatuto',1,'p_estatuto','ScannerParser.py',540),
  ('estatuto -> while','estatuto',1,'p_estatuto','ScannerParser.py',541),
  ('estatuto -> for','estatuto',1,'p_estatuto','ScannerParser.py',542),
  ('estatuto -> classcreate','estatuto',1,'p_estatuto','ScannerParser.py',543),
  ('estatuto -> vars','estatuto',1,'p_estatuto','ScannerParser.py',544),
  ('estatuto -> classdeclare','estatuto',1,'p_estatuto','ScannerParser.py',545),
  ('estatuto -> llamadafuncionclase','estatuto',1,'p_estatuto','ScannerParser.py',546),
  ('estatuto -> function','estatuto',1,'p_estatuto','ScannerParser.py',547),
  ('expresion -> m_exp','expresion',1,'p_expresion','ScannerParser.py',551),
  ('expresion -> m_exp expresion_a m_exp','expresion',3,'p_expresion','ScannerParser.py',552),
  ('expresion_a -> LT','expresion_a',1,'p_expresion_a','ScannerParser.py',560),
  ('expresion_a -> GT','expresion_a',1,'p_expresion_a','ScannerParser.py',561),
  ('expresion_a -> NE','expresion_a',1,'p_expresion_a','ScannerParser.py',562),
  ('expresion_a -> EQEQ','expresion_a',1,'p_expresion_a','ScannerParser.py',563),
  ('expresion_a -> LE','expresion_a',1,'p_expresion_a','ScannerParser.py',564),
  ('expresion_a -> GE','expresion_a',1,'p_expresion_a','ScannerParser.py',565),
  ('varcte -> ID','varcte',1,'p_varcte','ScannerParser.py',574),
  ('varcte -> CTE_I','varcte',1,'p_varcte','ScannerParser.py',575),
  ('varcte -> CTE_F','varcte',1,'p_varcte','ScannerParser.py',576),
  ('while -> while_b bloque','while',2,'p_while','ScannerParser.py',585),
  ('while_a -> WHILE','while_a',1,'p_while_a','ScannerParser.py',590),
  ('while_b -> while_a OP expresion CP','while_b',4,'p_while_b','ScannerParser.py',596),
  ('exp -> and_exp exp_a','exp',2,'p_exp','ScannerParser.py',601),
  ('exp_a -> OR','exp_a',1,'p_exp_a','ScannerParser.py',606),
  ('exp_a -> empty','exp_a',1,'p_exp_a','ScannerParser.py',607),
  ('and_exp -> expresion and_exp_a','and_exp',2,'p_and_exp','ScannerParser.py',611),
  ('and_exp_a -> AND','and_exp_a',1,'p_and_exp_a','ScannerParser.py',615),
  ('and_exp_a -> empty','and_exp_a',1,'p_and_exp_a','ScannerParser.py',616),
  ('for -> FOR OP asignacionsencilla SC expresion SC asignacionsencilla CP bloque','for',9,'p_for','ScannerParser.py',620),
  ('llamada -> ID OP llamada_a CP SC','llamada',5,'p_llamada','ScannerParser.py',624),
  ('llamada_a -> expresion llamada_b','llamada_a',2,'p_llamada_a','ScannerParser.py',630),
  ('llamada_a -> CTE_STRING llamada_b','llamada_a',2,'p_llamada_a','ScannerParser.py',631),
  ('llamada_a -> llamada_b','llamada_a',1,'p_llamada_a','ScannerParser.py',632),
  ('llamada_b -> COMMA llamada_a','llamada_b',2,'p_llamada_b','ScannerParser.py',638),
  ('llamada_b -> empty','llamada_b',1,'p_llamada_b','ScannerParser.py',639),
  ('fact -> fact_a exp CP','fact',3,'p_fact','ScannerParser.py',643),
  ('fact -> CTE_I','fact',1,'p_fact','ScannerParser.py',644),
  ('fact -> CTE_F','fact',1,'p_fact','ScannerParser.py',645),
  ('fact -> CTE_CHAR','fact',1,'p_fact','ScannerParser.py',646),
  ('fact -> ID','fact',1,'p_fact','ScannerParser.py',647),
  ('fact -> llamada','fact',1,'p_fact','ScannerParser.py',648),
  ('fact_a -> OP','fact_a',1,'p_fact_a','ScannerParser.py',657),
  ('classcreate -> CLASS CLASS_ID OB classcreate_a function classcreate_c CB','classcreate',7,'p_classcreate','ScannerParser.py',662),
  ('classcreate_a -> vars classcreate_a','classcreate_a',2,'p_classcreate_a','ScannerParser.py',670),
  ('classcreate_a -> vars_vect_mat classcreate_a','classcreate_a',2,'p_classcreate_a','ScannerParser.py',671),
  ('classcreate_a -> empty','classcreate_a',1,'p_classcreate_a','ScannerParser.py',672),
  ('classcreate_c -> function classcreate_d','classcreate_c',2,'p_classcreate_c','ScannerParser.py',676),
  ('classcreate_c -> classcreate_d','classcreate_c',1,'p_classcreate_c','ScannerParser.py',677),
  ('classcreate_d -> classcreate_c','classcreate_d',1,'p_classcreate_d','ScannerParser.py',681),
  ('classcreate_d -> empty','classcreate_d',1,'p_classcreate_d','ScannerParser.py',682),
  ('condicion -> IF OP expresion CP bloque condicion_a','condicion',6,'p_condicion','ScannerParser.py',686),
  ('condicion_a -> ELSE condicion_b bloque','condicion_a',3,'p_condicion_a','ScannerParser.py',690),
  ('condicion_b -> condicion','condicion_b',1,'p_condicion_b','ScannerParser.py',694),
  ('condicion_b -> empty','condicion_b',1,'p_condicion_b','ScannerParser.py',695),
  ('classdeclare -> CLASS_ID ID SC','classdeclare',3,'p_classdeclare','ScannerParser.py',698),
  ('llamadafuncionclase -> ID POINT llamada','llamadafuncionclase',3,'p_llamadafuncionclase','ScannerParser.py',702),
  ('asignacion -> ID asignacion_a asignacion_a EQ expresion SC','asignacion',6,'p_asignacion','ScannerParser.py',706),
  ('asignacion_a -> OSB exp CSB','asignacion_a',3,'p_asignacion_a','ScannerParser.py',716),
  ('asignacion_a -> empty','asignacion_a',1,'p_asignacion_a','ScannerParser.py',717),
  ('asignacionsencilla -> ID EQ expresion','asignacionsencilla',3,'p_asignacionsencilla','ScannerParser.py',721),
  ('function -> function_a ID OP function_b CP bloque','function',6,'p_function','ScannerParser.py',731),
  ('function_a -> VOID','function_a',1,'p_function_a','ScannerParser.py',740),
  ('function_a -> tiposimple','function_a',1,'p_function_a','ScannerParser.py',741),
  ('function_b -> tiposimple ID','function_b',2,'p_function_b','ScannerParser.py',750),
  ('function_b -> tiposimple ID COMMA function_b','function_b',4,'p_function_b','ScannerParser.py',751),
  ('function_b -> empty','function_b',1,'p_function_b','ScannerParser.py',752),
  ('empty -> <empty>','empty',0,'p_empty','ScannerParser.py',756),
]
