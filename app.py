import streamlit as st
import json

# Nastavenie stránky
st.set_page_config(page_title="Alza ID Extractor", page_icon="📦")

st.title("🔍 Location Sorting ID Extractor")
st.write("Vložte JSON text nižšie pre vytiahnutie ID zóny.")

# Textový vstup od používateľa
input_text = st.text_area("Vložte chybovú správu:", height=300, placeholder='{"QueryWatcherId": ...}')

if input_text:
    try:
        # Vyčistenie textu (ak by tam boli náhodné biele znaky na začiatku/konci)
        clean_text = input_text.strip()
        
        # Parsovanie JSONu
        data = json.loads(clean_text)
        
        # Získanie hodnoty
        target_id = data.get("@LocationSortingType_ID")
        
        if target_id is not None:
            st.success(f"Nájdené ID zóny:")
            st.code(target_id, language="text")
            
            # Bonus: Zobrazenie aj iných užitočných informácií
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Sorting Type ID", target_id)
            with col2:
                st.metric("Result Location Name", data.get("@ResultLocationName", "N/A"))
        else:
            st.warning("Kľúč '@LocationSortingType_ID' sa v texte nenachádza.")
            
    except json.JSONDecodeError:
        st.error("Chyba: Vložený text nie je platný JSON formát. Skontrolujte, či ste skopírovali celý objekt vrátane zložených zátvoriek { }.")
    except Exception as e:
        st.error(f"Vyskytla sa neočakávaná chyba: {e}")

st.divider()
st.caption("Interný nástroj pre Alza.cz | Vytvorené pomocou Streamlit")
