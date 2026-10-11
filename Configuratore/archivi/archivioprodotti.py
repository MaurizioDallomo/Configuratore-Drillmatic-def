from dati.creadati import crea_prodotto

class ArchivioProdotti:
    def __init__(self):
        self.elementi = {}

    def carica(self, catalogo):

        self.elementi["DXP10"] = crea_prodotto(
            catalogo, "1", "DXP10", "DXP", "75;150", "A;F;F1;L",
            "E|604|catena;F|604|catena;G|604|cinghia;H|604|cinghia;I|604|cinghia;J|403|cinghia;K|403|cinghia;L|403|cinghia;M|403|cinghia;N|203|cinghia;O|203|cinghia;P|203|cinghia;Q|203|cinghia;R|203|poly_v;S|203|poly_v;T|203|poly_v;U|203|poly_v;V|203|poly_v",
            None, "10mm", None, "1350N", None, "0,02mm", None, None, None, "80"
        )

        self.elementi["DXP18"] = crea_prodotto(
            catalogo, "1", "DXP18", "DXP", "100;150", "B;H;D1;N",
            "A|606|catena_riduttore;B|606|catena_riduttore;C|606|catena_riduttore;D|606|catena_riduttore;E|606|catena;F|606|catena;G|606|cinghia;H|606|cinghia;I|606|cinghia;J|406|cinghia;K|406|cinghia;L|406|cinghia;M|406|cinghia;N|205|cinghia;O|205|cinghia;P|205|cinghia;Q|205|cinghia;R|205|poly_v",
            None, "18mm", None, "4000N", None, "0,02mm", None, None, None, "112"
        )

        self.elementi["DXP24"] = crea_prodotto(
            catalogo, "1", "DXP24", "DXP", "120", "H1;S",
            "D|609|catena_riduttore;E|609|catena;F|609|catena;G|609|cinghia;H|609|cinghia;I|609|cinghia;J|407|cinghia;K|407|cinghia;L|407|cinghia;M|407|cinghia;N|207|cinghia;O|207|cinghia;P|207|cinghia;Q|207|cinghia",
            None, "24mm", None, "5500N", None, "0,02mm", None, None, None, "112",
            "cuscinetti;refrigerante"
        )

        self.elementi["DXE10"] = crea_prodotto(
            catalogo, "1", "DXE10", "DXE", "60;130", "A;F;L",
            "E|604|catena;F|604|catena;G|604|cinghia;H|604|cinghia;I|604|cinghia;J|403|cinghia;K|403|cinghia;L|403|cinghia;M|403|cinghia;N|203|cinghia;O|203|cinghia;P|203|cinghia;Q|203|cinghia;R|203|poly_v;S|203|poly_v;T|203|poly_v;U|203|poly_v;V|203|poly_v",
            None, "10mm", "M12", "1500N", None, "0,02mm", "Ø15x5mm", None, None, "80"
        )

        self.elementi["DXE16"] = crea_prodotto(
            catalogo, "1", "DXE16", "DXE", "90;130", "B;H;D1;N",
            "A|606|catena_riduttore;B|606|catena_riduttore;C|606|catena_riduttore;D|606|catena_riduttore;E|606|catena;F|606|catena;G|606|cinghia;H|606|cinghia;I|606|cinghia;J|406|cinghia;K|406|cinghia;L|406|cinghia;M|406|cinghia;N|205|cinghia;O|205|cinghia;P|205|cinghia;Q|205|cinghia;R|205|poly_v",
            None, "16mm", "M20", "5000N", None, "0,02mm", "Ø16x5mm", None, None, "112"
        )

        self.elementi["DXE23"] = crea_prodotto(
            catalogo, "1", "DXE23", "DXE", "115", "S;O",
            "D|606|catena_riduttore;E|606|catena;F|606|catena;G|606|cinghia;H|606|cinghia;I|606|cinghia;J|406|cinghia;K|406|cinghia;L|406|cinghia;M|406|cinghia;N|205|cinghia;O|205|cinghia;P|205|cinghia;Q|205|cinghia",
            None, "25mm", "M30", "7000N", None, "0,02mm", "Ø16x5mm", None, None, "112",
            "refrigerante"
        )

        self.elementi["DXE24"] = crea_prodotto(
            catalogo, "1", "DXE24", "DXE", "120", "H1;S",
            "D|609|catena_riduttore;E|609|catena;F|609|catena;G|609|cinghia;H|609|cinghia;I|609|cinghia;J|407|cinghia;K|407|cinghia;L|407|cinghia;M|407|cinghia;N|207|cinghia;O|207|cinghia;P|207|cinghia;Q|207|cinghia",
            None, "26mm", "M30", "7000N", None, "0,02mm", "Ø25x5mm", None, None, "112",
            "cuscinetti;refrigerante"
        )

        self.elementi["DXE42"] = crea_prodotto(
            catalogo, "1", "DXE42", "DXE", "160", "T",
            "A|609|catena_riduttore;B|609|catena_riduttore;C|609|catena_riduttore;D|407|catena_riduttore;E|407|catena_riduttore;F|407|catena_riduttore;G|609|cinghia;H|609|cinghia;I|609|cinghia;J|407|cinghia;K|407|cinghia;L|407|cinghia;M|407|cinghia;N|207|cinghia;O|207|cinghia;P|207|cinghia;Q|207|cinghia",
            None, "38mm", "M40", "9700N", None, "0,02mm", "Ø32x5mm", None, None, "112",
            "refrigerante"
        )

        self.elementi["TX12"] = crea_prodotto(
            catalogo, "1", "TX12", "TX", "50;100", "A;F;L",
            "A|604|catena_riduttore;A|704|catena_riduttore;B|604|catena_riduttore;B|704|catena_riduttore;C|604|catena_riduttore;C|704|catena_riduttore;D|604|catena_riduttore;D|704|catena_riduttore;E|604|catena;E|704|catena;F|604|catena;F|704|catena;G|604|cinghia;G|704|cinghia;H|604|cinghia;H|704|cinghia;I|604|cinghia;I|704|cinghia;J|403|cinghia;J|503|cinghia;K|403|cinghia;K|503|cinghia;L|403|cinghia;L|503|cinghia;M|403|cinghia;M|503|cinghia;N|203|cinghia;N|303|cinghia;O|203|cinghia;O|303|cinghia",
            None, None, "M12", None, None, None, None, None, None, "80"
        )

        self.elementi["TX20"] = crea_prodotto(
            catalogo, "1", "TX20", "TX", "80;100", "B;D;H;N",
            "A|606|catena_riduttore;A|706|catena_riduttore;B|606|catena_riduttore;B|706|catena_riduttore;C|606|catena_riduttore;C|706|catena_riduttore;D|606|catena_riduttore;D|706|catena_riduttore;E|606|catena;E|706|catena;F|606|catena;F|706|catena;G|606|cinghia;G|706|cinghia;H|606|cinghia;H|706|cinghia;I|606|cinghia;I|706|cinghia;J|406|cinghia;J|506|cinghia;K|406|cinghia;K|506|cinghia;L|406|cinghia;L|506|cinghia;M|406|cinghia;M|506|cinghia",
            None, None, "M20", None, None, None, None, None, None, "112"
        )

        self.elementi["TX28"] = crea_prodotto(
            catalogo, "1", "TX28", "TX", "80;120", "H2;I",
            "A2|609|cinghia;A2|709|cinghia;A|609|cinghia;A|709|cinghia;B|609|cinghia;B|709|cinghia;D|609|cinghia;D|709|cinghia;F|408|cinghia;F|508|cinghia;G|408|cinghia;G|508|cinghia",
            None, None, "M28", None, None, None, None, None, None, "112"
        )

        self.elementi["TX42"] = crea_prodotto(
            catalogo, "1", "TX42", "TX", "80;130", "I",
            "A2|609|catena;A2|709|catena;A|609|catena;A|709|catena;B|609|catena;B|709|catena;D|609|catena;D|709|catena;F|408|catena;F|508|catena;G|408|catena;G|508|catena",
            None, None, "M42", None, None, None, None, None, None, "112"
        )

        self.elementi["DTX12"] = crea_prodotto(
            catalogo, "1", "DTX12", "DTX", "75;150", "A;LC",
            "Z1|902|cinghia;Z2|901|cinghia;Z3|901|cinghia",
            None, None, "M12", None, None, None, None, None, None, "80"
        )

        self.elementi["DTX16"] = crea_prodotto(
            catalogo, "1", "DTX16", "DTX", "100;150", "B;LX",
            "Z1|902|cinghia;Z2|901|cinghia;Z3|901|cinghia",
            None, None, "M16", None, None, None, None, None, None, "112"
        )

        self.elementi["DX22"] = crea_prodotto(
            catalogo, "2", "DX22", "DX", None, "S;O",
            "G|606|cinghia;H|606|cinghia;I|606|cinghia;J|406|cinghia;K|406|cinghia;L|406|cinghia;M|406|cinghia;N|205|cinghia;O|205|cinghia;P|205|cinghia;Q|205|cinghia;R|205|poly_v;S|205|poly_v;T|205|poly_v;U|205|poly_v;V|205|poly_v",
            "RC;CO", "15mm", None, None, "2500N", "0,01mm", None, None, None, "90",
            "equilibratura"
        )

        self.elementi["DX28"] = crea_prodotto(
            catalogo, "2", "DX28", "DX", None, "P;Q;S;T",
            "E|606|catena;E|607|catena;F|606|catena;F|607|catena;G|606|cinghia;G|607|cinghia;H|606|cinghia;H|607|cinghia;I|606|cinghia;I|607|cinghia;J|406|cinghia;J|407|cinghia;K|406|cinghia;K|407|cinghia;L|406|cinghia;L|407|cinghia;M|407|cinghia;N|205|cinghia;N|207|cinghia;O|205|cinghia;O|207|cinghia;P|205|cinghia;P|207|cinghia;Q|205|cinghia;Q|207|cinghia;R|205|cinghia;R|207|cinghia;S|205|cinghia;S|207|cinghia;T|205|cinghia;T|207|cinghia;U|205|cinghia;U|207|cinghia;V|205|cinghia;V|207|cinghia",
            "RC;CO", "35mm", None, None, "9000N", "0,01mm", None, None, None, "112",
            "equilibratura;sbloccaggio_pneumatico;sbloccaggio_idraulico;predisposizione_teste"
        )

        self.elementi["DX38"] = crea_prodotto(
            catalogo, "2", "DX38", "DX", None, "P;Q;T;U",
            "A|609|catena_riduttore;A|611|catena_riduttore;B|609|catena_riduttore;B|611|catena_riduttore;C|609|catena_riduttore;C|611|catena_riduttore;D|407|catena_riduttore;D|410|catena_riduttore;E|407|catena_riduttore;E|410|catena_riduttore;F|407|catena_riduttore;F|410|catena_riduttore;G|609|cinghia;G|611|cinghia;H|609|cinghia;H|611|cinghia;I|609|cinghia;I|611|cinghia;J|407|cinghia;J|410|cinghia;K|407|cinghia;K|410|cinghia;L|407|cinghia;L|410|cinghia;M|407|cinghia;M|410|cinghia;N|207|cinghia;N|209|cinghia;O|207|cinghia;O|209|cinghia;P|207|cinghia;P|209|cinghia",
            "RC;CO", "50mm", None, None, "15000N", "0,01mm", None, None, None, "132",
            "equilibratura;sbloccaggio_pneumatico;sbloccaggio_idraulico"
        )

        self.elementi["DX38L"] = crea_prodotto(
            catalogo, "2", "DX38L", "DX", None, "TL",
            "A|609|catena_riduttore;A|611|catena_riduttore;B|609|catena_riduttore;B|611|catena_riduttore;C|609|catena_riduttore;C|611|catena_riduttore;D|407|catena_riduttore;D|410|catena_riduttore;E|407|catena_riduttore;E|410|catena_riduttore;F|407|catena_riduttore;F|410|catena_riduttore;G|609|cinghia;G|611|cinghia;H|609|cinghia;H|611|cinghia;I|609|cinghia;I|611|cinghia;J|407|cinghia;J|410|cinghia;K|407|cinghia;K|410|cinghia;L|407|cinghia;L|410|cinghia;M|407|cinghia;M|410|cinghia;N|207|cinghia;N|209|cinghia;O|207|cinghia;O|209|cinghia;P|207|cinghia;P|209|cinghia",
            "RC;CO", "50mm", None, None, "15000N", "0,01mm", None, None, None, "132",
            "equilibratura;sbloccaggio_pneumatico;sbloccaggio_idraulico"
        )

        self.elementi["DX58"] = crea_prodotto(
            catalogo, "2", "DX58", "DX", None, "P;U",
            "A|611|catena_riduttore;B|611|catena_riduttore;C|611|catena_riduttore;D|412|catena_riduttore;E|412|catena_riduttore;F|412|catena_riduttore;G|611|cinghia;H|611|cinghia;I|611|cinghia;J|412|cinghia;K|412|cinghia;L|412|cinghia;M|412|cinghia;N|213|cinghia;O|213|cinghia;P|213|cinghia",
            "RC;CO", "50mm", None, None, "25000N", "0,01mm", None, None, None, "180",
            "sbloccaggio_pneumatico;sbloccaggio_idraulico"
        )

        self.elementi["DX88"] = crea_prodotto(
            catalogo, "2", "DX88", "DX", None, "U",
            "G|612|cinghia;H|612|cinghia;I|612|cinghia;J|411|cinghia;K|411|cinghia;L|411|cinghia;M|411|cinghia;N|210|cinghia;O|210|cinghia;P|210|cinghia",
            "RC;CO", "60mm", None, None, "40000N", "0,01mm", None, None, None, "180",
            "sbloccaggio_pneumatico;sbloccaggio_idraulico"
        )

        self.elementi["EX28"] = crea_prodotto(
            catalogo, "3", "EX28", "EX", "100;200;300",
            None, None, None, None, None, "7000N", None, None, "Ø20x5mm",
            None, None, None, "soffietto_100;soffietto_200;soffietto_300"
        )

        self.elementi["EX32"] = crea_prodotto(
            catalogo, "3", "EX32", "EX", "250;400",
            None, None, None, None, None, "9000N", None, None, "Ø25x5mm",
            None, None, None, "soffietto_250;soffietto_400"
        )

        self.elementi["EX38"] = crea_prodotto(
            catalogo, "3", "EX38", "EX", "200;300;400;600",
            None, None, None, None, None, "21400N", None, None, "Ø40x5mm",
            None, None, None, "soffietto_200;soffietto_300;soffietto_400;soffietto_600"
        )

        self.elementi["EX58"] = crea_prodotto(
            catalogo, "3", "EX58", "EX", "300",
            None, None, None, None, None, "21400N", None, None, "Ø40x5mm",
            None, None, None, "soffietto_300"
        )

        self.elementi["HX38"] = crea_prodotto(
            catalogo, "3", "HX38", "HX", "200;300",
            None, None, None, None, None, "15500N", None, None, None,
            None, "63", None, "soffietto_200;soffietto_300"
        )

        self.elementi["PX28"] = crea_prodotto(
            catalogo, "3", "PX28", "HX", "150",
            None, None, None, None, None, "4500N", None, None, None,
            "63"
        )

    def get_prodotto(self, prodotto):
        return self.elementi.get(prodotto)
            
    def elenco(self):
        return self.elementi