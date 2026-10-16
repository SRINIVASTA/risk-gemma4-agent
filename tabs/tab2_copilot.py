import streamlit as st

def render(engine, min_threshold):
    st.header("💬 Conversational CoCo Copilot")
    st.caption("Query real-time network liabilities and trace policy intersections interactively using Gemma 4.")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]): st.markdown(message["content"])

    if user_prompt := st.chat_input("Ask CoCo about current ledger anomalies..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"): st.markdown(user_prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("CoCo is tracing policy vectors via Gemma 4..."):
                try:
                    reference_df = engine.detect_signals(min_amount=min_threshold)
                    reference_df.columns = reference_df.columns.str.strip().str.upper()
                    policy_context = engine.gather_evidence(reference_df)
                    
                    cleaned_prompt = str(user_prompt).strip().upper()
                    matched_mask = reference_df['ACCOUNT_ID'].astype(str).str.contains(cleaned_prompt, case=False, na=False) | reference_df['CUSTOMER_NAME'].astype(str).str.contains(cleaned_prompt, case=False, na=False)
                    filtered_df = reference_df[matched_mask]
                    
                    columns_to_show = ['TRANSACTION_ID', 'ACCOUNT_ID', 'CUSTOMER_NAME', 'AMOUNT', 'COUNTRY_CODE', 'RISK_SCORE', 'KYC_STATUS', 'IS_PEP']
                    data_matrix_payload = filtered_df[columns_to_show].to_string(index=False) if not filtered_df.empty else reference_df[columns_to_show].head(40).to_string(index=False)
                    
                    chat_template = f"You are 'CoCo' an elite Compliance Copilot powered by Gemma 4.\n\nDATA MATRIX:\n{data_matrix_payload}\n\nCONTEXT:\n{policy_context}\n\nUser Query: {user_prompt}"
                    active_tier = str(st.session_state.get("active_thinking_level", "MINIMAL")).upper()
                    
                    from google.genai import types
                    response = engine.client.models.generate_content(
                        model='gemma-4-26b-a4b-it', contents=chat_template,
                        config=types.GenerateContentConfig(
                            system_instruction="Speak concisely and format metrics into clear tables.",
                            temperature=0.1, thinking_config=types.ThinkingConfig(thinking_level=active_tier), max_output_tokens=2000
                        )
                    )
                    assistant_response = response.text
                    st.markdown(assistant_response)
                except Exception as chat_err:
                    assistant_response = f"❌ Inference Exception: {str(chat_err)}"
                    st.error(assistant_response)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
