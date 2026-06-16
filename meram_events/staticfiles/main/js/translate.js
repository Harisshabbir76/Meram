/**
 * Meram Events — Complete Bilingual Translation System
 * Covers: Home, About, Gallery, FAQ, Contact, Book Now, Services, Corporate, Other Services
 * Strategy: Walk every text node in <main>/<section>/<article> and translate it.
 *           Skips SVG, <script>, <style>, <input> values.
 *           Preserves HTML structure — only text nodes are touched.
 */

/* ============================================================
   FULL TRANSLATION MAP  (English → Arabic)
   Key   = EXACT English text as it appears trimmed in the HTML
   Value = Arabic translation
============================================================ */
const AR = {

  /* ── NAVBAR ────────────────────────────── */
  "About":                          "حول",
  "Services":                       "الخدمات",
  "Gallery":                        "المعرض",
  "All Services":                   "جميع الخدمات",
  "Corporate Events":               "فعاليات الشركات",
  "Other Services":                 "خدمات أخرى",
  "Book Now":                       "احجز الآن",
  "Home":                           "الرئيسية",
  "Contact":                        "اتصل بنا",
  "FAQ":                            "أسئلة شائعة",

  /* ── FOOTER ────────────────────────────── */
  "MERAM EVENTS IS A LUXURY EVENT PLANNING AND DESIGN HOUSE DEDICATED TO CRAFTING REFINED WEDDINGS, ENGAGEMENTS, AND PRIVATE GATHERINGS ACROSS THE UAE.":
    "ميرام إيفنتس هي دار تخطيط فعاليات فاخرة متخصصة في تنظيم حفلات الأعراس والخطوبة والتجمعات الخاصة الراقية في الإمارات العربية المتحدة.",
  "• ABOUT US":                     "• من نحن",
  "• SERVICES":                     "• الخدمات",
  "• GALLERY":                      "• المعرض",
  "• FAQ":                          "• أسئلة شائعة",
  "• CONTACT US":                   "• اتصل بنا",
  "FOLLOW US ON:":                  "تابعنا على:",
  "© 2026 MERAM EVENTS":            "© 2026 ميرام إيفنتس",

  /* ── HOME PAGE ─────────────────────────── */
  "Where Refined Celebrations Come to Life":
    "حيث تتجسّد الاحتفالات الراقية",
  "Bespoke weddings, engagements, and private events designed with precision, elegance, and unforgettable detail.":
    "أعراس وخطوبات وفعاليات خاصة مصممة بدقة وأناقة وتفاصيل لا تُنسى.",
  "Plan Your Event":                "خطط لفعاليتك",
  "Book a Consultation":            "احجز استشارة",
  "Crafting Experiences Beyond Expectations":
    "إبداع تجارب تفوق التوقعات",
  "With a complete 360° approach, every event is thoughtfully conceptualized, expertly planned, and flawlessly executed — ensuring a seamless journey from vision to reality.":
    "بنهج شامل 360°، يُصمَّم كل حدث بتأنٍّ، ويُخطَّط باحترافية، ويُنفَّذ بإتقان — لضمان رحلة سلسة من الفكرة إلى الواقع.",
  "With years of experience in luxury weddings, engagements, and private celebrations, we transform moments into timeless experiences defined by elegance, precision, and intentional design.":
    "بسنوات من الخبرة في الأعراس الفاخرة والخطوبة والاحتفالات الخاصة، نحوّل اللحظات إلى تجارب خالدة تتسم بالأناقة والدقة والتصميم الهادف.",
  "View Gallery":                   "مشاهدة المعرض",
  "Wedding & Event Planning":       "تخطيط الأعراس والفعاليات",
  "Floral & Decor Design":          "تصميم الزهور والديكور",
  "VIP Hospitality":                "الضيافة الفاخرة",
  "Explore Our Services":           "استكشف خدماتنا",
  "Why Choose Meram Events":        "لماذا تختار ميرام إيفنتس",
  "A Seamless Experience Designed Around You":
    "تجربة متكاملة مصممة حول رغباتك",
  "Personalized concepts tailored to your vision":
    "مفاهيم مخصصة تتوافق مع رؤيتك",
  "Full-service planning from start to finish":
    "تخطيط شامل من البداية حتى النهاية",
  "Refined aesthetic with attention to detail":
    "ذوق راقٍ مع الاهتمام بكل تفصيلة",
  "Trusted execution at luxury venues":
    "تنفيذ موثوق في أفخم الأماكن",
  "Dedicated team ensuring flawless coordination":
    "فريق متخصص يضمن تنسيقًا لا تشوبه شائبة",
  "You Know, It's Time To":         "حان الوقت",
  "Create a Celebration That Reflects Your Story Like Never Before.":
    "أنشئ احتفالًا يعكس قصتك كما لم يحدث من قبل.",
  "Let's create your moment":       "دعنا نصنع لحظتك",
  "↑ Back to Top":                  "↑ العودة للأعلى",

  /* ── ABOUT PAGE ────────────────────────── */
  "About Us":                       "من نحن",
  "WE DON'T JUST PLAN EVENTS. WE CREATE EXPERIENCES THAT STAY WITH YOU.":
    "لا نخطط للأحداث فحسب. نصنع تجارب تبقى معك.",
  "We Don't Just Plan Events. We Create Experiences That Stay With You.":
    "لا نخطط للأحداث فحسب. نصنع تجارب تبقى معك.",
  "At Meram Events, every celebration begins with a story — yours.":
    "في ميرام إيفنتس، كل احتفال يبدأ بقصة — قصتك.",
  "A Thoughtful Approach to Every Detail.":
    "نهج متأنٍّ لكل تفصيلة.",
  "Founded with a passion for elevated celebrations, Meram Events has built a reputation for delivering high-end experiences that balance artistry with organisation.":
    "تأسست ميرام إيفنتس بشغف لتقديم احتفالات راقية، وبنت سمعتها في تقديم تجارب فاخرة تجمع بين الإبداع الفني والتنظيم الاحترافي.",
  "From intimate gatherings to grand weddings, our team approaches every event with intention — carefully curating each element to reflect the client's vision while maintaining a cohesive and refined aesthetic.":
    "من التجمعات الحميمة إلى الأعراس الكبرى، يتعامل فريقنا مع كل حدث بقصد واضح — نختار كل عنصر بعناية ليعكس رؤية العميل مع الحفاظ على جمالية متماسكة وراقية.",
  "\"We believe that true luxury lies in the details you don't have to worry about.\"":
    "\"نؤمن أن الرفاهية الحقيقية تكمن في التفاصيل التي لا تحتاج للقلق بشأنها.\"",
  "We believe that true luxury lies in the details you don't have to worry about.":
    "نؤمن أن الرفاهية الحقيقية تكمن في التفاصيل التي لا تحتاج للقلق بشأنها.",
  "Designed with Intention, Delivered with Precision.":
    "مصمم بقصد، منفَّذ بدقة.",
  "We believe every event should feel effortless — even though it is anything but.":
    "نؤمن أن كل حدث يجب أن يبدو سهلًا — حتى وإن لم يكن كذلك.",
  "Our philosophy is centred on creating experiences that are:":
    "فلسفتنا تتمحور حول خلق تجارب:",
  "Deeply personal and tailored":   "شخصية وعميقة ومخصصة",
  "Visually refined and cohesive":  "جميلة بصريًا ومتناسقة",
  "Seamlessly executed from start to finish":
    "منفذة بسلاسة من البداية للنهاية",
  "Emotionally resonant and memorable":
    "ذات وقع عاطفي ولا تُنسى",
  "Because the most beautiful celebrations are not just seen — they are felt.":
    "لأن أجمل الاحتفالات لا تُرى فحسب — بل تُحسّ.",
  "Our Experience":                 "خبرتنا",
  "Trusted Across the UAE's Leading Venues":
    "موثوق به في أبرز أماكن الإمارات",
  "Over the years, Meram Events has delivered premium celebrations across some of the UAE's most prestigious venues, including Beach Rotana, Rixos Marina, Hilton Yas Island, Waldorf Astoria, W Hotel, and Damac. These collaborations reflect our consistent commitment to excellence, attention to detail, and the ability to execute at the highest standards.":
    "على مر السنين، قدمت ميرام إيفنتس احتفالات راقية في أبرز أماكن الإمارات، منها بيتش روتانا، وريكسوس مارينا، وهيلتون جزيرة ياس، وولدورف أستوريا، وفندق W، وداماك. تعكس هذه الشراكات التزامنا الثابت بالتميز والاهتمام بالتفاصيل.",
  "Our Values":                     "قيمنا",
  "At Meram Events, Trust Isn't Optional — It's the Foundation of Everything We Do.":
    "في ميرام إيفنتس، الثقة ليست خيارًا — إنها أساس كل ما نقوم به.",
  "We operate with a high level of professionalism, sharp attention to detail, and a commitment to getting every element right from first contact to final execution. Our focus is clear: deliver a smooth experience, handle everything with precision, and represent every event at its best.":
    "نعمل بمستوى عالٍ من الاحترافية والانتباه الدقيق للتفاصيل والالتزام بإتقان كل عنصر من أول تواصل حتى التنفيذ النهائي. هدفنا واضح: تقديم تجربة سلسة والتعامل مع كل شيء بدقة.",
  "What We Do Differently":         "ما يميزنا",
  "More Than Planning, A Complete Experience.":
    "أكثر من تخطيط، تجربة متكاملة.",
  "We take a 360° approach to every event, managing everything from concept and design to guest experience and on-site coordination.":
    "نتبع نهجًا شاملًا 360° لكل حدث، ندير فيه كل شيء من الفكرة والتصميم إلى تجربة الضيوف والتنسيق الميداني.",
  "This means:":                    "هذا يعني:",
  "You don't have to manage multiple vendors":
    "لا تحتاج لإدارة موردين متعددين",
  "Every detail is aligned and cohesive":
    "كل تفصيلة متوافقة ومتناسقة",
  "The entire experience feels seamless":
    "التجربة بأكملها تشعر بالسلاسة",
  "You can fully enjoy your event without stress":
    "يمكنك الاستمتاع الكامل بحدثك بلا ضغط",
  "Because your only focus should be the moment itself.":
    "لأن تركيزك الوحيد يجب أن يكون على اللحظة ذاتها.",
  "Your Story, Beautifully Told.":  "قصتك، تُروى بجمال.",
  "At Meram Events, We Don't Believe in One-Size-Fits-All Celebrations.":
    "في ميرام إيفنتس، لا نؤمن بالاحتفالات النمطية.",
  "Book a Call Now":                "احجز مكالمة الآن",
  "Book a Call Now ›":              "احجز مكالمة الآن ›",

  /* ── SERVICES PAGE ─────────────────────── */
  "Our Services":                   "خدماتنا",
  "Crafted for the Extraordinary":  "مصمم للاستثنائي",
  "What We Offer":                  "ما نقدمه",
  "A Complete 360° Event Experience":
    "تجربة فعاليات متكاملة 360°",
  "From concept to execution, our team handles every element of your celebration with expertise, creativity, and an unwavering commitment to excellence.":
    "من الفكرة إلى التنفيذ، يتولى فريقنا كل عنصر في احتفالك بخبرة وإبداع والتزام راسخ بالتميز.",
  "Wedding & Event Planning":       "تخطيط الأعراس والفعاليات",
  "Your wedding is a once-in-a-lifetime occasion, and we treat it as such. Our wedding planning service provides complete management of every detail, from venue selection to final send-off.":
    "زفافك مناسبة لمرة واحدة في العمر، ونتعامل معها بهذه الأهمية. تشمل خدمتنا إدارة كاملة لكل تفصيلة من اختيار المكان حتى التوديع الأخير.",
  "Venue scouting & selection":     "البحث عن الأماكن واختيارها",
  "Full timeline management":       "إدارة شاملة للجدول الزمني",
  "Vendor coordination":            "تنسيق الموردين",
  "Day-of coordination":            "تنسيق يوم الحدث",
  "Guest management & logistics":   "إدارة الضيوف واللوجستيات",
  "Book a Consultation":            "احجز استشارة",
  "Floral & Decor Design":          "تصميم الزهور والديكور",
  "Our in-house design team creates breathtaking floral arrangements and bespoke decor that transform any space into an immersive, unforgettable environment.":
    "يبتكر فريق التصميم الداخلي لدينا تنسيقات زهور آسرة وديكورات مخصصة تحوّل أي مكان إلى بيئة غامرة لا تُنسى.",
  "Custom floral arrangements":     "تنسيقات زهور مخصصة",
  "Table & centerpiece design":     "تصميم الطاولات والمحوريات",
  "Lighting design & installation": "تصميم الإضاءة وتركيبها",
  "Ceremony & reception backdrops": "خلفيات حفلات الزفاف والاستقبال",
  "Full venue transformation":      "تحويل شامل للمكان",
  "VIP Hospitality":                "الضيافة الفاخرة",
  "For clients who demand the pinnacle of luxury, our VIP hospitality service delivers a seamlessly curated experience with exclusive access, private arrangements, and world-class service.":
    "لعملائنا الذين يطلبون أعلى مستويات الفخامة، تقدم خدمة الضيافة الراقية تجربة منسقة بشكل مثالي مع وصول حصري وترتيبات خاصة وخدمة على مستوى عالمي.",
  "Private venue arrangements":     "ترتيبات المكان الخاص",
  "Luxury transportation":          "المواصلات الفاخرة",
  "Exclusive catering curation":    "انتقاء الضيافة الحصرية",
  "Personal concierge service":     "خدمة الكونسيرج الشخصي",
  "Security & privacy management":  "إدارة الأمن والخصوصية",
  "Engagement Ceremonies":          "حفلات الخطوبة",
  "Mark your new chapter with a beautifully orchestrated engagement celebration. We design intimate yet stunning events that honor the beginning of your love story.":
    "أطلق فصلك الجديد باحتفال خطوبة منسق بشكل جميل. نصمم فعاليات حميمة ومبهرة تكرّم بداية قصة حبك.",
  "Proposal planning & styling":    "تخطيط وتنسيق الخطبة",
  "Engagement party design":        "تصميم حفلة الخطوبة",
  "Announcement experiences":       "تجارب الإعلان",
  "Photography moment curation":    "انتقاء لحظات التصوير",

  /* ── GALLERY PAGE ──────────────────────── */
  "A Collection of Moments, Beautifully Brought to Life":
    "مجموعة من اللحظات، أُحييت بجمال",
  "Here we invite you to step inside ours. Explore a curated collection of weddings, engagements, and private events designed and executed by Meram Events across the UAE — each one a reflection of elegance, intention, and refined detail.":
    "ندعوك هنا للدخول إلى عالمنا. استكشف مجموعة منتقاة من الأعراس والخطوبة والفعاليات الخاصة التي صممتها وأقامتها ميرام إيفنتس في الإمارات — كل واحدة منها انعكاس للأناقة والهدف والتفاصيل الراقية.",
  "From breathtaking installations to intimate table settings, every image here is a testament to our commitment to creating experiences that feel as extraordinary as they look.":
    "من التركيبات الآسرة إلى إعدادات الطاولات الحميمة، كل صورة هنا شاهدة على التزامنا بإنشاء تجارب تشعر باستثنائيتها كما تبدو عليها.",
  "Every celebration tells a story...":
    "كل احتفال يروي قصة...",
  "A Collection of Moments":        "مجموعة من اللحظات",
  "Beautifully Brought to Life":    "أُحييت بجمال",
  "Designed with Intention":        "مصمم بقصد",
  "Where Every Detail Matters":     "حيث تهم كل تفصيلة",
  "LET'S CREATE SOMETHING WORTH REMEMBERING.":
    "لنخلق شيئًا يستحق الذكر.",
  "Let's Create Something Worth Remembering.":
    "لنخلق شيئًا يستحق الذكر.",
  "Inspired by what you see? Let us design a celebration that reflects your vision and exceeds your expectations.":
    "مستوحى مما رأيته؟ دعنا نصمم احتفالًا يعكس رؤيتك ويتجاوز توقعاتك.",
  "Book a Call Now":                "احجز مكالمة الآن",
  "Follow us on Instagram to view more of what we are doing...":
    "تابعنا على إنستغرام لمزيد من أعمالنا...",
  "You Know It's Time To":          "حان الوقت",
  "Create a Celebration That Reflects Your Story Like Never Before.":
    "أنشئ احتفالًا يعكس قصتك كما لم يحدث من قبل.",

  /* ── FAQ PAGE ──────────────────────────── */
  "Everything You Need to Know":    "كل ما تحتاج معرفته",
  "BEFORE WE BEGIN SOMETHING UNFORGETTABLE.":
    "قبل أن نبدأ شيئًا لا يُنسى.",
  "Before We Begin Something Unforgettable.":
    "قبل أن نبدأ شيئًا لا يُنسى.",
  "Planning a celebration of this scale comes with questions — and it should. We've curated the most important details below to guide you through what it's like to work with Meram Events, what to expect, and how we ensure every experience feels seamless, personal, and beautifully executed.":
    "التخطيط لاحتفال بهذا الحجم يأتي مع أسئلة — وهذا طبيعي. لقد جمعنا أهم التفاصيل أدناه لإرشادك حول كيفية العمل مع ميرام إيفنتس وما يمكن توقعه وكيف نضمن أن تكون كل تجربة سلسة وشخصية ومنفذة بشكل جميل.",
  "FREQUENTLY ASKED QUESTIONS":     "الأسئلة الشائعة",
  "Frequently Asked Questions":     "الأسئلة الشائعة",
  "When should we start planning our event?":
    "متى يجب أن نبدأ التخطيط لفعاليتنا؟",
  "Do you only specialise in weddings?":
    "هل تتخصصون في حفلات الزفاف فقط؟",
  "Weddings are at the heart of what we do, but our expertise extends to engagements and private celebrations as well. Each event is approached with the same level of creativity, precision, and elevated design — regardless of scale.":
    "الأعراس في صميم ما نقوم به، لكن خبرتنا تمتد أيضًا إلى حفلات الخطوبة والاحتفالات الخاصة. نتعامل مع كل فعالية بنفس مستوى الإبداع والدقة والتصميم الراقي.",
  "Do you offer full-service planning?":
    "هل تقدمون خدمة التخطيط الشامل؟",
  "Yes. We offer comprehensive end-to-end planning, from concept development and vendor sourcing to on-the-day coordination. We also offer partial planning and design-only packages depending on your needs.":
    "نعم. نقدم تخطيطًا شاملًا من الألف إلى الياء، من تطوير المفهوم وانتقاء الموردين إلى التنسيق يوم الحدث. نقدم أيضًا باقات تخطيط جزئي أو تصميم فقط حسب احتياجاتك.",
  "Can you work with our preferred venue or suppliers?":
    "هل يمكنكم العمل مع المكان أو الموردين المفضلين لدينا؟",
  "Absolutely. We're happy to collaborate with your chosen venue or existing suppliers while bringing our coordination expertise to ensure everything runs seamlessly.":
    "بالتأكيد. يسعدنا التعاون مع مكانك المختار أو الموردين الحاليين مع إضافة خبرتنا التنسيقية لضمان سير كل شيء بسلاسة.",
  "What makes Meram Events different?":
    "ما الذي يميز ميرام إيفنتس؟",
  "We combine a deeply personalised approach with a high level of design sensibility and operational precision. Every event we produce is a reflection of your unique story — not a template. We take pride in creating experiences that feel effortless for you and extraordinary for your guests.":
    "نجمع نهجًا شخصيًا عميقًا مع مستوى عالٍ من الحساسية التصميمية والدقة التشغيلية. كل فعالية ننتجها هي انعكاس لقصتك الفريدة — لا نموذج جاهز.",
  "Do you handle guest experience and coordination?":
    "هل تتولون تجربة الضيوف والتنسيق؟",
  "Yes. Guest experience is a core part of our service — from arrival logistics and seating arrangements to hospitality coordination and flow management throughout the event.":
    "نعم. تجربة الضيوف جزء أساسي من خدمتنا — من لوجستيات الوصول وترتيبات الجلوس إلى تنسيق الضيافة وإدارة سير الفعالية.",
  "Can you create custom décor and floral concepts?":
    "هل يمكنكم ابتكار ديكور وزهور مخصصة؟",
  "Yes. Our in-house design team works closely with you to develop a bespoke visual concept — including floral design, table styling, lighting, and full venue transformation — tailored specifically to your aesthetic.":
    "نعم. يعمل فريق التصميم الداخلي لدينا معك عن كثب لتطوير مفهوم بصري مخصص يشمل تصميم الزهور وتنسيق الطاولات والإضاءة والتحويل الكامل للمكان.",
  "How do we begin working with you?":
    "كيف نبدأ العمل معكم؟",
  "Simply reach out through our contact page or book a call. We'll arrange an initial consultation to understand your vision, share our approach, and outline how we can bring your celebration to life.":
    "تواصل معنا عبر صفحة الاتصال أو احجز مكالمة. سنرتب استشارة أولية لفهم رؤيتك ومشاركة نهجنا وتوضيح كيف يمكننا إحياء احتفالك.",
  "For weddings and large-scale events, we recommend starting the planning process 9–12 months in advance to ensure the best availability of venues and suppliers. For smaller celebrations, 3–6 months is typically sufficient.":
    "للأعراس والفعاليات الكبيرة، نوصي ببدء التخطيط قبل 9-12 شهرًا لضمان أفضل توفر للأماكن والموردين. للاحتفالات الأصغر، 3-6 أشهر عادةً كافية.",
  "Still Have Questions?":          "هل لا تزال لديك أسئلة؟",
  "We'd Love to Hear from You.":    "يسعدنا الاستماع إليك.",
  "Let's begin with a conversation — and take the first step toward creating something truly unforgettable.":
    "لنبدأ بمحادثة — ونتخذ الخطوة الأولى نحو خلق شيء لا يُنسى حقًا.",
  "Contact Us Now":                 "اتصل بنا الآن",

  /* ── CONTACT PAGE ──────────────────────── */
  "CONTACT US":                     "اتصل بنا",
  "Contact Us":                     "اتصل بنا",
  "LET'S BEGIN SOMETHING BEAUTIFUL":
    "لنبدأ شيئًا جميلًا",
  "Let's Begin Something Beautiful": "لنبدأ شيئًا جميلًا",
  "EVERY UNFORGETTABLE CELEBRATION BEGINS WITH A CONVERSATION.":
    "كل احتفال لا يُنسى يبدأ بمحادثة.",
  "Every unforgettable celebration begins with a conversation.":
    "كل احتفال لا يُنسى يبدأ بمحادثة.",
  "WHETHER YOU'RE PLANNING A WEDDING, AN ENGAGEMENT, OR A PRIVATE EVENT, WE WOULD LOVE TO UNDERSTAND YOUR VISION AND EXPLORE HOW WE CAN BRING IT TO LIFE — WITH ELEGANCE, PRECISION, AND CARE.":
    "سواء كنت تخطط لزفاف أو خطوبة أو فعالية خاصة، يسعدنا فهم رؤيتك واستكشاف كيف يمكننا تحقيقها — بأناقة ودقة واهتمام.",
  "Whether you're planning a wedding, an engagement, or a private event, we would love to understand your vision and explore how we can bring it to life — with elegance, precision, and care.":
    "سواء كنت تخطط لزفاف أو خطوبة أو فعالية خاصة، يسعدنا فهم رؤيتك واستكشاف كيف يمكننا تحقيقها — بأناقة ودقة واهتمام.",
  "Share a few details with us, and our team will be in touch to guide you through the next steps.":
    "شاركنا بعض التفاصيل وسيتواصل معك فريقنا لإرشادك في الخطوات التالية.",
  "SEND MESSAGE":                   "إرسال الرسالة",
  "Send Message":                   "إرسال الرسالة",

  /* ── BOOK NOW PAGE ─────────────────────── */
  "Book Now":                       "احجز الآن",
  "Begin Your Journey":             "ابدأ رحلتك",
  "Start Planning":                 "ابدأ التخطيط",
  "Let's Create Something Extraordinary":
    "لنخلق شيئًا استثنائيًا",
  "Fill out the form and one of our event specialists will contact you within 24 hours to discuss your vision.":
    "أكمل النموذج وسيتواصل معك أحد متخصصي الفعاليات في غضون 24 ساعة لمناقشة رؤيتك.",
  "Submit Your Request":            "أرسل طلبك",
  "Tell us about your event vision and requirements.":
    "أخبرنا عن رؤيتك ومتطلبات فعاليتك.",
  "Initial Consultation":           "الاستشارة الأولية",
  "We'll schedule a meeting to discuss your vision in detail.":
    "سنحدد موعدًا لمناقشة رؤيتك بالتفصيل.",
  "Custom Proposal":                "عرض مخصص",
  "Receive a tailored proposal crafted specifically for your event.":
    "احصل على عرض مصمم خصيصًا لفعاليتك.",
  "Begin Planning":                 "ابدأ التخطيط",
  "Once approved, we begin crafting your perfect event.":
    "بعد الموافقة، نبدأ في صياغة فعاليتك المثالية.",
  "Request a Booking":              "طلب حجز",
  "All fields marked * are required":"جميع الحقول المميزة * مطلوبة",
  "Personal Information":           "المعلومات الشخصية",
  "Event Details":                  "تفاصيل الفعالية",
  "Submit Booking Request":         "إرسال طلب الحجز",

  /* ── CORPORATE EVENTS ──────────────────── */
  "Corporate Events":               "فعاليات الشركات",
  "Professional. Prestigious. Precise.": "احترافي. مرموق. دقيق.",
  "Corporate Excellence":           "التميز في فعاليات الشركات",
  "Elevating Your Brand Through Events":
    "ترقية علامتك التجارية من خلال الفعاليات",
  "From product launches to gala dinners, board retreats to award ceremonies — Meram Events brings the same level of luxury and precision to the corporate world that we apply to our finest private celebrations.":
    "من إطلاق المنتجات إلى حفلات العشاء الراقية، ومن اجتماعات مجلس الإدارة إلى حفلات الجوائز — تجلب ميرام إيفنتس نفس مستوى الفخامة والدقة إلى عالم الشركات.",
  "We understand that corporate events are an extension of your brand identity. Our team works closely with you to ensure every element reflects your organization's values, culture, and objectives.":
    "نفهم أن فعاليات الشركات هي امتداد لهويتك التجارية. يعمل فريقنا معك عن كثب لضمان أن كل عنصر يعكس قيم مؤسستك وثقافتها وأهدافها.",
  "Request a Proposal":             "طلب عرض",
  "Corporate Event Services":       "خدمات فعاليات الشركات",
  "Award Ceremonies":               "حفلات الجوائز",
  "Prestigious award nights designed to honor achievement with elegance and grandeur.":
    "ليالي جوائز مرموقة مصممة لتكريم الإنجازات بأناقة وفخامة.",
  "Product Launches":               "إطلاق المنتجات",
  "Impactful launch events that create buzz and leave a lasting brand impression.":
    "فعاليات إطلاق مؤثرة تخلق ضجة وتترك انطباعًا دائمًا للعلامة التجارية.",
  "Gala Dinners":                   "حفلات العشاء الراقية",
  "Sophisticated dining experiences with world-class cuisine and refined ambiance.":
    "تجارب طعام راقية مع مأكولات عالمية المستوى وأجواء متميزة.",
  "Conferences":                    "المؤتمرات",
  "Professional conference setups blending functionality with elevated aesthetics.":
    "إعدادات مؤتمرات احترافية تجمع بين الوظيفية والجماليات الراقية.",
  "Our Corporate Work":             "أعمالنا في فعاليات الشركات",
  "Past Events":                    "الفعاليات السابقة",

  /* ── OTHER SERVICES ────────────────────── */
  "Beyond the Ordinary":            "ما وراء العادي",
  "Floral & Decor Design":          "تصميم الزهور والديكور",
  "Our in-house floristry team creates extraordinary arrangements. From delicate table centerpieces to dramatic ceremony installations, every bloom is selected and placed with intention.":
    "يبتكر فريق تنسيق الزهور الداخلي لدينا ترتيبات استثنائية. من المحوريات الرقيقة للطاولات إلى التركيبات الدرامية للحفلات، كل زهرة تُختار وتُوضع بقصد.",
  "Exclusive":                      "حصري",
  "Bespoke hospitality management for discerning clients. Private lounges, exclusive access, curated menus, and white-glove service from arrival to departure.":
    "إدارة ضيافة مخصصة لعملاء مميزين. صالات خاصة ووصول حصري وقوائم طعام منتقاة وخدمة فاخرة من الوصول حتى المغادرة.",
  "Private":                        "خاص",
  "Intimate Gatherings":            "التجمعات الحميمة",
  "Not every celebration needs to be grand. We design intimate, deeply personal events — dinner parties, family milestones, anniversary celebrations — with the same care as our largest events.":
    "ليس كل احتفال بحاجة لأن يكون ضخمًا. نصمم فعاليات حميمة وشخصية عميقة — حفلات عشاء ومناسبات عائلية واحتفالات بالذكرى السنوية — بنفس الاهتمام الذي نوليه لأضخم فعالياتنا.",
  "Ready?":                         "هل أنت مستعد؟",
  "Let's Create Something Extraordinary Together":
    "لنخلق معًا شيئًا استثنائيًا",
};

/* Reverse map: Arabic → English */
const EN = {};
Object.entries(AR).forEach(([en, ar]) => { EN[ar] = en; });

/* ============================================================
   CORE ENGINE
============================================================ */
let currentLang = localStorage.getItem('meramLang') || 'en';

/**
 * Walk every text node under `root` and replace text
 * according to the provided dictionary.
 */
function translateNodes(root, dict) {
  // Tags whose text we should NEVER touch
  const SKIP_TAGS = new Set(['SCRIPT','STYLE','SVG','PATH','NOSCRIPT','TEXTAREA']);

  function walk(node) {
    if (node.nodeType === Node.TEXT_NODE) {
      const raw = node.textContent;
      const trimmed = raw.trim();
      if (!trimmed) return;

      // Try full trimmed text first
      if (dict[trimmed] !== undefined) {
        // Preserve leading/trailing whitespace
        node.textContent = raw.replace(trimmed, dict[trimmed]);
        return;
      }

      // Try sentence-by-sentence inside the text node
      // (handles cases where one text node has a few words)
      let replaced = raw;
      // Sort keys longest-first so "A B C" matches before "A B"
      const keys = Object.keys(dict).sort((a,b) => b.length - a.length);
      for (const key of keys) {
        if (replaced.includes(key)) {
          replaced = replaced.split(key).join(dict[key]);
        }
      }
      if (replaced !== raw) node.textContent = replaced;

    } else if (node.nodeType === Node.ELEMENT_NODE) {
      if (SKIP_TAGS.has(node.tagName)) return;
      // Also skip input/button values set via value attr
      for (const child of node.childNodes) walk(child);
    }
  }
  walk(root);
}

/** Translate placeholder attributes */
function translatePlaceholders(dict) {
  document.querySelectorAll('[placeholder]').forEach(el => {
    const val = el.getAttribute('placeholder');
    if (dict[val]) el.setAttribute('placeholder', dict[val]);
  });
}

/** Translate data-en / data-ar attributes */
function translateDataAttrs(lang) {
  document.querySelectorAll('[data-en],[data-ar]').forEach(el => {
    const target = el.getAttribute('data-' + lang);
    if (!target) return;
    if (el.children.length === 0) {
      el.textContent = target;
    }
  });
}

/** Main language switcher — called from footer buttons */
function setLang(lang) {
  currentLang = lang;
  localStorage.setItem('meramLang', lang);

  const html = document.getElementById('html-root');
  const labelEl = document.getElementById('lang-label');
  const enBtn = document.getElementById('lang-en-btn');
  const arBtn = document.getElementById('lang-ar-btn');
  const wrap = document.getElementById('lang-wrap');

  if (lang === 'ar') {
    html.setAttribute('dir', 'rtl');
    html.setAttribute('lang', 'ar');
    if (labelEl) labelEl.textContent = 'عربي';
    if (enBtn) enBtn.classList.remove('active');
    if (arBtn) arBtn.classList.add('active');
    // Translate entire body
    translateNodes(document.body, AR);
    translatePlaceholders(AR);
    translateDataAttrs('ar');
  } else {
    html.setAttribute('dir', 'ltr');
    html.setAttribute('lang', 'en');
    if (labelEl) labelEl.textContent = 'ENGLISH';
    if (arBtn) arBtn.classList.remove('active');
    if (enBtn) enBtn.classList.add('active');
    // Translate back to English
    translateNodes(document.body, EN);
    translatePlaceholders(EN);
    translateDataAttrs('en');
  }

  // Close dropdown
  if (wrap) wrap.classList.remove('open');
}

/* Apply saved language when page loads */
document.addEventListener('DOMContentLoaded', () => {
  if (currentLang === 'ar') {
    setLang('ar');
  }
});
