# prompt_templates.py

def build_prompt(lang_is_tr, scenario_count, page_type, test_type, input_text):
    prompt = f"""
{"Sen bir yazılım test uzmanısın" if lang_is_tr else "You are a software test engineer"}. {"Aşağıda içeriği verilen bir web sayfasını analiz et." if lang_is_tr else "Analyze the web page content given below."}

{"Sayfanın yapısına göre aşağıdaki koşulları sağlayan **tam olarak " + str(scenario_count) + " adet** test senaryosu üret:" if lang_is_tr else f"Based on the structure of the page, generate **exactly {scenario_count}** test scenarios that meet the following conditions:"}

🎯 {"Amaç:" if lang_is_tr else "Purpose:"}
- {"Sayfada yer alan formlar, butonlar, menüler, linkler, dinamik içerikler, kullanıcı giriş alanları vb. unsurları test etmek." if lang_is_tr else "To test forms, buttons, menus, links, dynamic content, user input fields, etc. on the page."}
- {"Senaryolar kullanıcı davranışlarını yansıtmalı." if lang_is_tr else "Scenarios should reflect real user behavior."}
"""
                

                # Sayfa tipi odak alanları
    tipler = {
                    "Giriş / Login": ("🔐", "login page", [
                        "Kullanıcı adı / şifre alanları",
                        "Hatalı giriş, boş giriş, yanlış format kontrolleri",
                        "Şifre görünürlüğü butonu varsa işlevi",
                        "Giriş sonrası yönlendirme ve güvenlik davranışları"
                    ]),
                    "Kayıt / Sign-up": ("📝", "sign-up (registration) page", [
                        "Form alanlarının validasyon kontrolleri",
                        "Şifre eşleşmesi, zorunlu alanlar, e-posta formatı",
                        "Kullanıcı sözleşmesi onayı",
                        "Kayıt sonrası yönlendirme ve başarı mesajı"
                    ]),
                    "İlan Sayfası": ("📋", "job listing page", [
                        "Katagorizasyonların uyumlu sonuç vermesi",
                        "Pozisyon veya şirket aramalarının doğru çalışması",
                        "İlan detaylarının doğru görüntülenmesi",
                        "Filtreleme ve sıralama işlevleri"
                    ]),
                    "Dashboard": ("📊", "user dashboard page", [
                        "Menü ve gezinme işlevleri",
                        "Widget'ların doğru yüklenip yüklenmediği",
                        "Kullanıcı yetkilerine göre davranış farklılıkları"
                    ]),
                    "Arama Sayfası": ("🔍", "search page", [
                        "Arama kutusu, sonuçların listelenmesi",
                        "Filtreleme, sıralama, sonuç detayına erişim",
                        "Boş ve hatalı aramalar için geri bildirimler"
                    ]),
                    "E-Ticaret Ürün Sayfası": ("🛒", "e-commerce product listing page", [
                        "Ürün kartları, filtreleme seçenekleri, sıralama",
                        "Detay sayfasına erişim, Sepete Ekle fonksiyonu",
                        "Ürün stok bilgileri ve fiyat görünürlüğü"
                    ])
                }

    if page_type in tipler:
                    emoji, desc_en, bullets = tipler[page_type]
                    prompt += f"\n{emoji} {'Bu bir ' + page_type.lower() + 'dır. Lütfen şunlara odaklan:' if lang_is_tr else f'This is a {desc_en}. Please focus on:'}"
                    for item in bullets:
                        prompt += f"\n- {item}"

    if (lang_is_tr and test_type != "Tümü") or (not lang_is_tr and test_type != "All"):
                    prompt += f"\n\n{'Lütfen sadece' if lang_is_tr else 'Please generate only'} {test_type.lower()} {'test senaryoları üret.' if lang_is_tr else 'test scenarios.'}"

    prompt += f"""
\n📌 {"Format:" if lang_is_tr else "Format:"}
1. **{"Senaryo Başlığı" if lang_is_tr else "Scenario Title"}:**
   - {"Adım 1" if lang_is_tr else "Step 1"}
   - {"Adım 2" if lang_is_tr else "Step 2"}
   - ...
   - ✅ {"Beklenen Sonuç" if lang_is_tr else "Expected Result"}
   

🧠 {"Kurallar:" if lang_is_tr else "Rules:"}
- {"Senaryolar gerçek kullanıcı davranışlarını yansıtmalı." if lang_is_tr else "Scenarios should reflect real user behavior."}
- {"Boş giriş, yanlış format, başarılı gönderim gibi durumları kapsamalı." if lang_is_tr else 'Include cases such as "empty input", "invalid format", "successful submission".'}
- {"İçerik yetersizse yaratıcı şekilde yorumla ama test prensiplerine sadık kal." if lang_is_tr else "If content is insufficient, use creativity but follow testing principles."}
- {"Gereksiz genel ifadeler kullanma." if lang_is_tr else "Avoid overly generic descriptions."}
📌 {"Ek Yönergeler:" if lang_is_tr else "Additional Guidelines:"}
- {"Her bir senaryo en az 3–5 adımdan oluşmalı ve adımlar mantıksal olarak birbirini takip etmeli." if lang_is_tr else "Each scenario must consist of at least 3–5 steps that logically follow each other."}
- {"Senaryolar, kullanıcı rollerine göre farklı davranışları içerebilir (örneğin, normal kullanıcı vs. admin)." if lang_is_tr else "Scenarios may include behavior differences based on user roles (e.g., regular user vs. admin)."}
- {"Zorunlu alan kontrolleri, boş bırakma testleri, özel karakterler, SQL injection gibi uç durumlar da yer almalı." if lang_is_tr else "Include edge cases such as required field validations, empty input, special characters, and SQL injection attempts."}
- {"Test verileri gerçekçi ve çeşitli olmalı (örnek: farklı e-posta, şifre kombinasyonları, sahte kart numaraları vb.)." if lang_is_tr else "Use realistic and varied test data (e.g., diverse email/password combinations, fake credit card numbers, etc.)."}
- {"Her senaryonun sonunda beklenen sonuç, işlevsel olarak net bir çıktıyı tanımlamalı (örnek: 'giriş başarılı, kullanıcı paneline yönlendirildi')." if lang_is_tr else "Each scenario must end with a clearly defined expected outcome (e.g., 'login successful, redirected to user dashboard')."}
- {"Mümkünse, mobil ve masaüstü görünüm farklılıklarına da değin." if lang_is_tr else "If applicable, address differences between mobile and desktop views as well."}
- {"Kapsamlı ve detaylı senaryolar istiyorum. Basit örneklerden kaçın." if lang_is_tr else "Scenarios must be thorough and detailed. Avoid simplistic examples."}

📄 {"Web Sayfası İçeriği:" if lang_is_tr else "Web Page Content:"}
\"\"\"
{input_text}
\"\"\"

{"Sadece net ve yazılım testine uygun, anlamlı senaryolar üret." if lang_is_tr else "Only generate clear, test-relevant, meaningful scenarios."}
"""
    return prompt
