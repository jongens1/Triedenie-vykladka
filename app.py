import streamlit as st
import json

# Nastavenie stránky
st.set_page_config(page_title="Alza ID Extractor", page_icon="🔍", layout="centered")

st.title("🔍 Location Sorting ID Extractor")
st.info("Vložte JSON nižšie pre analýzu typu triedenia a ID zóny.")

# Textový vstup
input_text = st.text_area("Vložte chybovú správu:", height=250, placeholder='{"QueryWatcherId": ...}')

if input_text:
    try:
        # Parsovanie JSONu
        data = json.loads(input_text.strip())
        
        # Extrakcia kľúčových hodnôt zo sekcie RESULTS
        sorting_type_id = data.get("@LocationSortingType_ID")
        utilized_sort_type = data.get("@UtilizedSortType")  # RAMP / UNLOADING
        super_type_id = data.get("@LocationSortingSuperType_ID")
        location_name = data.get("@ResultLocationName", "Neznáma lokalita")

        st.subheader("📊 Výsledok analýzy")

        # 1. Hlavné ID zóny (LocationSortingType_ID)
        st.metric(label="Location Sorting Type ID", value=sorting_type_id)

        # 2. Rozlíšenie RAMP vs UNLOADING
        col1, col2 = st.columns(2)
        
        with col1:
            if utilized_sort_type == "RAMP":
                st.warning(f"🚀 Typ: **EXPEDIČNÉ** ({utilized_sort_type})")
            elif utilized_sort_type == "UNLOADING":
                st.info(f"📥 Typ: **VÝKLADKOVÉ** ({utilized_sort_type})")
            else:
                st.write(f"Typ: {utilized_sort_type}")

        with col2:
            st.write(f"📍 **Lokácia:** {location_name}")

        # 3. Logika pre SuperType (ak je to výkladka alebo ak existuje)
        st.divider()
        
        if utilized_sort_type == "UNLOADING":
            st.write("### 🧩 Detail pre výkladku")
            if super_type_id is not None:
                st.success(f"**Location Sorting SuperType ID:** `{super_type_id}`")
                st.caption("Toto ID určuje zoskupovanie medzi pravidlami v číselníku.")
            else:
                st.warning("SuperType ID nie je v tomto JSON-e definované (null).")
        else:
            # Ak je to RAMP, môžeme SuperType zobraziť len ako doplnkový údaj ak existuje
            if super_type_id:
                st.write(f"Doplnkové SuperType ID: `{super_type_id}`")

    except json.JSONDecodeError:
        st.error("❌ Chyba: Vložený text nie je platný JSON. Skontrolujte, či ste skopírovali celý text.")
    except Exception as e:
        st.error(f"❌ Vyskytla sa chyba: {e}")

st.sidebar.markdown("""
### Ako to funguje:
1. **@LocationSortingType_ID**: Základné ID zóny.
2. **@UtilizedSortType**: 
    - `RAMP` = Expedičné triedenie.
    - `UNLOADING` = Výkladkové triedenie.
3. **@LocationSortingSuperType_ID**: V prípade nadradeného pravidla ukáže nadradené ID
""")
