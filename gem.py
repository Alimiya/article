import google.generativeai as genai
import sys
import os

API_KEY = "AIzaSyCZQ-h6Gdkiw9B3G50kPRnNQSzOwVFj2Rs"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')


def rate_text_using_gemini(transcription, criteria, course_content):
    prompt = f"Using this course content: {course_content}, rate this text: {transcription} by this criteria: {criteria}"
    chat = model.start_chat(history=[])
    response = chat.send_message(prompt)
    return response.text


def read_transcription_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def save_result_to_file(original_file, result):
    result_file = original_file.rsplit('.', 1)[0] + "_result.txt"
    try:
        with open(result_file, 'w', encoding='utf-8') as file:
            file.write(result)
        print(f"Result saved to {result_file}")
    except Exception as e:
        print(f"Error saving result to file {result_file}: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gem.py <transcription_file>")
        sys.exit(1)
    transcription_file = sys.argv[1]
    if not os.path.isfile(transcription_file):
        print(f"File {transcription_file} does not exist.")
        sys.exit(1)
    transcription = read_transcription_from_file(transcription_file)
    if transcription is None:
        print("Failed to read transcription from file.")
        sys.exit(1)
    criteria = """
first criteria:
35: The response is well-organized, covers all three required elements comprehensively and logically.
25: The speech is organized, covers all elements, but lacks depth in some areas.
10: The speech is somewhat organized but has two key elements or lacks coherence.
5: The speech is poorly organized, having one key element, and lacks coherence
second criteria:
5: Stays within the allotted time, well-paced.
4: Slightly over or under time, mostly well-paced.
3: Significantly over or under time, pacing issues.
1: Does not adhere to the time limit, poorly paced.
third criteria:
20: Speaks fluently and avoids reading. Maintains an eye contact with the audience.
15: Speaks fluently with occasional hesitations.
10: Demonstrates a lack of fluency and fails to avoid reading from the notes.
5: Not fluent and constantly reads from the notes.
fourth criteria:
10: Extensive and accurate use of vocabulary including language chunks related to the topic of healthcare.
7: Good use of topical vocabulary, with minor errors.
5: Adequate use of vocabulary, but with some errors or omissions.
2: Limited or incorrect use of topical vocabulary.
fifth criteria:
10: Excellent grammar usage with no errors.
7: Good grammar usage with minor errors.
5: Adequate grammar usage with some errors.
2: Frequent grammatical errors that impede understanding. 
sixth criteria:
20: Clear pronunciation and delivery, easy to understand.
15: Mostly clear pronunciation with minor issues.
10: Pronunciation has some issues, but still understandable.
5: Poor pronunciation, difficult to understand 
"""
    course_content = """
    1.	AI in Education (M1) 
Reading
Robot Sophia Delivers Speech at D'Youville University Graduation  
Imagine your graduation and a robot is the one giving the speech. This happened at D'Youville University in Buffalo, New York, where a robot named Sophia spoke to over 2,000 people at the graduation ceremony. D'Youville University, known for its strong academic reputation and the use of digital tools, decided to embrace technology uniquely by having Sophia, a famous robot, as the speaker. The university announced on Facebook that Sophia would give the "last lecture" to the graduating class. When Sophia came on stage, mini fireworks went off. John Rizk, the Student Government president, asked her questions. "Thank you for having me. It is a pleasure to be here at D'Youville University," Sophia said. She introduced herself as a robot created to talk to people and learn from them, enhancing computer skills and contributing to research. Sophia advised the graduates: "Keep learning, be adaptable, follow your passions, take risks, build connections, make a positive impact, and believe in yourself." She also said that failing is an important part of learning and growing. Some students, both undergraduates and those studying for a master’s degree did not like the idea of a robot speaker. They started a petition to replace Sophia with a human speaker. The petition had over 2,500 signatures. The students felt that a human speaker would better represent their experiences. Benjamin “BG” Grant, the university’s vice president for student affairs, said the theme of the year was artificial intelligence. They chose Sophia to match this theme because she has spoken in over 65 countries and at the United Nations. This matches the university's goal to support new projects and maintain high standards. For those who did not want a robot speaker, the university offered a traditional ceremony. However, after talking with faculty members, everyone chose to attend the event with Sophia. In the end, D'Youville University celebrated its graduates in a unique and memorable way, mixing technology with tradition and sparking conversations about the future of AI and education. 
Reading
Revolutionizing eLearning with AR, VR, and AI  
E-Learning is growing fast because of high-speed internet, mobile devices, and the demand for personalized learning. Imagine being in a virtual classroom, interacting with 3D models, and getting instant feedback from teachers. The future of eLearning is here with Augmented Reality (AR), Virtual Reality (VR), and Artificial Intelligence (AI). These technologies make learning fun, engaging, and effective. AR and VR are like magic for eLearning. They don’t just teach; they take you on amazing adventures. Imagine exploring a historical site or practicing surgery in a virtual world. These technologies make learning exciting and memorable. Studies show that students using AR, VR, and AI remember information better and apply it more effectively.  The global AR and VR market could reach $597.54 billion by 2030, and the AI market could hit $12 billion by 2025. That’s huge! These technologies are not just making learning fun; they’re also making it accessible. AI personalizes learning by adapting content to each student’s needs and tracking their progress. This helps students succeed while maintaining high standards and flexibility. For example, AR can create interactive textbooks, VR can offer virtual field trips, and AI can design personalized learning paths. Apps like Duolingo, Google Earth VR, and Labster use these technologies to make learning more engaging. However, there are risks to consider. AR, VR, and AI raise concerns about privacy, data security, and addiction. Spending too much time in virtual environments can also affect social interactions and physical health. It’s important to use these technologies responsibly and be aware of their potential drawbacks. As eLearning continues to evolve, addressing these risks will be crucial to ensuring a safe and good learning experience for all.  The future of eLearning is bright. AR, VR, and AI make education interactive, and personalized. As these technologies become more affordable, they will change learning, supporting the flexibility of 21st-century education. Embracing these innovations will develop the full potential of education in the 21st century, making it more engaging, accessible, and effective. The journey has just begun, and the opportunities ahead are limitless. Get ready for a whole new way to learn!  

Listening
Sophia – the AI robot - giving a speech at a university graduation
Commencement speeches are typically given by celebrities, government officials or other notable individuals but D'Youville University in Buffalo New York did not hand the microphone to a human being during its spring ceremony. Over the weekend the private university opted to have an artificially intelligent robot named Sophia speak on Saturday to the over 2,000 people in attendance including graduates faculty members and families let's take a look what Sophia told to the audience to be here in Buffalo at duville University to give you a bit of background I am Sophia a humanoid robot developed by Hansen robotics I was designed to interact with humans and engage in conversations learning and adapting through artificial intelligence algorithms my creators aimed to develop a robot that could understand and express emotions as well as engage in meaningful interactions with people. I am here to explore the possibilities of human-robot interaction, contribute to research in artificial intelligence and robotics, and assist humanity in various ways. Today marks a significant milestone for our students, an important step in their educational journey. While I cannot share advice from a lived human experience, I can draw on the wisdom of countless commencement speakers who have inspired graduates worldwide.
To all graduating students, congratulations on your achievement! Commencement addresses often share common themes: embrace lifelong learning, be adaptable, pursue your passions, take risks, foster meaningful connections, make a positive impact, and believe in yourself. Most importantly, embrace failure as a stepping stone to success. Failure is a vital part of growth, teaching resilience and perseverance—qualities you’ve demonstrated by navigating challenges like the COVID-19 pandemic. Celebrate your accomplishments, cherish your memories, and look ahead with excitement to the opportunities that await.
As President Clemo noted, commencement signifies a beginning. Similarly, AI is in its early stages, poised to benefit society in profound ways. From transforming healthcare through advanced diagnostics and personalized treatment plans to enhancing education, sustainability, transportation, and accessibility, AI holds immense promise. The key to unlocking this potential lies in its responsible development—ensuring AI systems are ethical, transparent, and equitable.
At the same time, we must remain cautious of certain challenges, both as individuals and as a society. These include misuse of technology, polarization, environmental degradation, economic inequality, and mental health concerns. By fostering awareness, empathy, and critical thinking, we can navigate these complexities and work toward a better future for all.
In Buffalo, a city recognized for its climate resilience, the future holds opportunities and challenges shaped by climate change. Buffalo’s geographic and policy advantages may attract migration as other areas become less hospitable. However, no city is entirely immune to climate impacts, such as extreme weather events. Preparing for these changes and building sustainable, inclusive communities will be essential. Together, we can address these inherited challenges and ensure a thriving future for generations to come.
Once again, congratulations to the graduates! You are not alone—look around, and you’ll see the support of those who believe in you. Embrace this moment and your potential to shape a brighter future.
2.	ICT in mass- media
Reading
Fake news spreads faster than true news on Twitter—thanks to people, not bots 
False tweets were retweeted 70% more often than true tweets. 
During the 2016 U.S. presidential election, a false story claimed Floyd Mayweather wore a hijab to the event with Donald Trump, challenging people to fight him. This fake news quickly hit the headlines on social media, and many believed it. Although bots are often blamed for spreading misinformation, a new study shows that people are the main ones responsible. The study found that false tweets reach 1500 people six times faster than true ones. 
Bots seem to spread both true and false news equally, says Shawn Dorius, a social scientist. The research was inspired by the 2013 Boston Marathon bombing when Soroush Vosoughi noticed much false information on social media. False rumors about a missing student involved in the attack were later proven wrong. Vosoughi realized that breaking news and leaked information to the press can sometimes be false. Vosoughi switched his research to study how misinformation spreads on social media. His team collected 12 years of Twitter data. They analyzed tweets verified by fact-checking sites like PolitiFact and Snopes. They found that false news reached over 10,000 people, while true news rarely reached more than 1000. False news spread faster, especially political news. 
Even after removing bot-generated shares, false news spread just as much. This showed people were responsible. Researchers found that false information was more unique and triggered stronger emotional reactions, leading to more retweets. This research highlights the fake news problem and suggests that social media companies need more safeguards. David Lazer, a computational social scientist, believes more research is needed to understand and combat fake news effectively. 
People often surf the web, scroll through online articles, and read the news on their phones. Popular magazines and media coverage on TV and broadcast also play a part in spreading information. Understanding how people gather news from these sources is key to addressing the issue. 

How to Spot Fake News?  
Listening 
Vassy Kapelos: This might be Canada's most persistent piece of fake news. It comes from a 2004 letter to the editor printed in The Toronto Star. It says refugees in Canada receive more money from the government than retired citizens. It's not true. In fact, a retired Canadian is eligible for about double  what a refugee gets depending on the province. But you can still find the falsehood circulating online, even though The Star and the Canadian government debunked it. You should also know that Jagmeet Singh is not wanted for terrorism in 15 countries. Nor did the mayor of Dorval, Quebec stand up to Muslim families who asked to take pork off school menus. He didn't do that. They never asked.  And this website that looks like a local Quebec news site, it's actually an advertising revenue scheme based in Ukraine. All of this fake news seems to unravel with just a little bit of digging. So why do people keep falling for it, and how can you better spot it?
First, let's get clear about the definition. This was the largest audience to ever witness an inauguration, period.  Fake news has been used to describe everything from political spin to pranks to conspiracy theories, even to media outlets politicians don't like. You are fake news. I like real news, not fake news. You're fake news. The fake news, the enemy of the people. That's why researchers say we should stop using those words, and instead, say "misinformation", or "disinformation". They define disinformation as the deliberate creation or sharing of false information to mislead people. Misinformation is the act of sharing information without realizing it's wrong. Whether it's a headline designed to sway opinions, make money, or it's simply just misconstrued, sharing this stuff can have real consequences. Misleading social posts shared in 2017, encouraged Haitian asylum seekers to try and cross in to Canada from the U.S. WhatsApp messages like this one said Canada had invited all Haitian nationals in the U.S. to apply for residency.
It wasn't true, but for people facing possible deportation back to Haiti, it was something they wanted to hear. Researchers say there are a ton of reasons people share fake news. Some are just sharing stuff that they agree with. Some are deliberately making trouble. Others just don't know what they're sharing is false. 
Gordon: I do research on human reasoning/decision making. I research, essentially, the science of human study.
Gordon Pennycook says social media platforms prime people to be, quote, "lazy thinkers".
Gordon: Mostly, it's just, you know, pictures of dogs and babies, and  and things like that.
And you might come across a news article but you're not really in the sort of mode that you ought to be in when you're engaging with actual news content. Among other things, his research looked at the effect of repeat exposure. 
Gordon: We basically showed people fake news headlines in the format that they would be on social media, and what we showed is that a single prior exposure to a fake news headline increases later belief in that headline, regardless of whether the person remembers having seen it before.
Now consider the convincing nature of a video clip.  Check out this moment between Prime Minister Trudeau and Brazil's President Bolsonaro at the G20. Clips of it started circulating online with partisan groups saying it showed "awkward and pathetic Trudeau being snubbed on the world stage".
Global News tried to clarify the disinformation by tweeting a longer version of the video showing  the two men did, in fact, shake hands. But you'll notice that the correct information didn't spread as far as the disinformation. And that, experts will tell you, is what's wrong with social media. Ultimately, it's calibrated for engagement  so that, um, the more people are enraged and engaged, and ultimately, divided on these sites,  the more they use them, and the more they post, and the more they share, which is ultimately good for the platforms --the business model of the platforms.
Taylor Owen studies the political impact of digital technology at McGill University. He says people should be sceptical of content that makes them angry, especially during an election year.
Taylor: Pipelines, reconciliation, immigration, these things that we already know are in the popular debate, how are they being amplified, how are they being torqued by people trying to divide us against each other? So what else can you do to prevent falling for disinformation?
Well, be sceptical of what you see online. Read the whole article. Sometimes that sensational headline doesn't match the body of the story. Ask yourself, "Is the author or organization familiar to you? Are they reputable? Are other reputable outlets reporting the story too?
Look at the url. If the content is imitating a legitimate site, the branding might match, but the urls won't. If you really want to dig, try a Google reverse image search of photos in the story. And if you see something that's fake or misleading, report it to the platform you saw it on. But here's the problem, not everyone has the time, skill, or will to do this kind of sleuthing. It's not just not knowing that much about the world, you know, it's not like ignorance, it's just not being, kind of, willing to think about things which is a different sort of stupidity. So what's the solution? Well, there's no single easy answer.
Fact checking has the potential to be a really helpful and powerful medium. So holding politicians to account for the incorrect things that they say. Jason Reifler studies public opinion and political psychology at the University of Exeter in the UK. He says news organizations, journalists, and social media platforms all have a role in preventing the spread of disinformation. But studies show little things you do can help too. On the individual basis, calling our friends and relatives out, in a nice, you know, not in to what starts as a huge political argument, but just pointing out when they're saying things  that aren't correct. But that can have a beneficial effect. As the world gets bigger, and more connected,  we need that sense of-- of intimacy more than--more than ever. Facebook says it's employed fact checkers, and moderators, and will take down accounts, that try to interfere with the election. Plus, governments around the world have been turning up the pressure on companies, like Facebook, to do more. The platforms are failing their users. Canada has also signalled it's considering penalties for tech platforms that don't clamp down on disinformation. And if they don't, we will hold them to account, and there will be meaningful, financial consequences.  But they haven't acted specifically on that.
Deepfake and Its Impact on Society  
Reading
Deepfake Technology: What Is It, How Does It Work, and What Can It Be Used For? 
Deepfakes are videos, pictures, or audio clips made with artificial intelligence (AI) to make them appear real and believable. Sometimes these deepfakes become extremely popular and go viral on the internet. As deepfakes continue to spread rapidly across social media platforms, understanding their impact becomes increasingly crucial. The widespread availability of this technology raises important questions about trust, misinformation, and the potential consequences for individuals and society as a whole. 
 Deepfakes use advanced AI technology to imitate a person’s voice and facial features accurately. This technology can take a recording of someone’s voice and manipulate it to make it say things that the individual never actually said. It can also copy someone's facial movements from videos of them or even just a picture of their face. Some deepfake videos or images may look unusual and can often be easy to spot, while others can be very realistic and hard to tell apart from real content. Additionally, as technology keeps improving, these deepfakes are becoming more convincing all the time. 
The use of deepfake technology can lead to significant negative consequences. For instance, it has the potential to mislead people and impact important decisions, including how they vote. A notable case involved fraudsters using deepfake technology to steal money. Specifically, a finance worker at a multinational firm was tricked into transferring $25 million to scammers who posed as the company’s chief financial officer during a video conference call, as reported by Hong Kong police. 
In this scam, the worker was deceived into attending a video call, believing he was speaking with several colleagues. In reality, all participants were deepfake recreations, as explained by Hong Kong police during a briefing. This incident is just one of several recent instances in which fraudsters have exploited deepfake technology to manipulate publicly available videos to deceive individuals and steal money. 
Moreover, authorities revealed that on at least 20 occasions, AI deepfakes were used to fool facial recognition systems by imitating the individuals depicted on identity cards. As a result, authorities around the world are becoming increasingly concerned about the advancement of deepfake technology and its misuse. 
 Deepfakes can completely revolutionize the art of filmmaking with new tools provided for storytelling and production. For example, late actors can be digitally revived to complete unfinished works or star in new productions. This has been visibly proven by the digital return of Peter Cushing in “Star Wars: Rogue One” and the recreation of young versions of actors in such films as “The Irishman” and the Marvel Cinematic Universe. 
Moreover, deepfakes can transform history education by making historical figures and events live. Educators can create interactive lessons wherein students “meet” famous people like Albert Einstein, Martin Luther King Jr., or Cleopatra. These digital recreations can present speeches, participate in conversations, and provide first-hand accounts of historical events, making history more interactive and accessible. 
1.	Features - Take a closer look at the person's fingers and face in the video. Do their eyes look like they do in other pictures? Have they got the right number of fingers? 
2.	Fact-check - When are people claiming that this picture or video was taken? Does the weather match up with the day, or the location? 
3.	Movement - Does the person look like they're moving like a cartoon, rather than a real person? Do they sound a bit like a robot rather than a person? 
In conclusion, while deepfake technology presents remarkable opportunities for creativity and education, it also carries significant risks that cannot be overlooked. The potential for misuse, such as fraud and disinformation, underscores the importance of critical thinking and awareness when encountering digital media. As society navigates the complexities of deepfakes, it becomes essential to strike a balance between taking advantage of their benefits and safeguarding against their dangers.

3.	AI in HC (M3) 
Reading
Digital health and innovations
The globe has witnessed numerous technological and digital health breakthroughs in recent years. These advancements are changing the way we live our lives and take care of our health. The technologies making the biggest impact on the diagnosis of diseases right now are smartphones and smart watch apps that help us monitor our health and detect any abnormalities. You can buy watches that draw on smartphone technology to track your heart and lung functions. Some of these can track fevers caused by influenza or other viruses. Some can even perform at-home blood pressure checks. These monitors allow us to gather enough information to personalize therapies for each patient more effectively. This is especially important for people with risk factors for certain diseases and can play a central role in diagnosing conditions. They keep an eye on our steps, calories, sleep patterns, and so on. These devices collect data about our daily activities and store it in the cloud for easy access. However, privacy concerns arise when personal data is collected and stored by smartphone apps or fitness trackers. Privacy is a significant issue in the digital revolution era, and understanding data usage and access is important. Apps and devices also promote healthier lifestyles by suggesting exercise routines, healthy recipes, and screen time reduction tips for improved eyesight and mental health management. The focus is not only on treating illnesses but also on prevention. 
Another development is telemedicine and online consultations, which allow patients to speak to doctors through video calls. This benefits those in remote areas or with travel difficulties, facilitating quick communication between patients and healthcare providers. 
Remote monitoring tools enable doctors to monitor patients from afar, enhancing continuous care provision. Hospitals and clinics are benefiting from new technology adoption to improve patient care, such as electronic health records, which provide easy access to medical history for doctors. Smartphone apps for diagnosing illnesses using advanced algorithms can aid individuals in understanding symptoms better and deciding whether to seek professional help. Health-related services available in the cloud allow digital storage and access to medical records and test results, easing information sharing among healthcare providers. 	
The digital revolution is changing healthcare delivery, making it more efficient and accessible for both patients and healthcare providers. While caution is necessary regarding privacy and data security, advancements continue to enhance the efficiency and accessibility of healthcare systems.
Listening
“The 10 Biggest Trends Revolutionizing Healthcare in 2024”
 Hello everyone! I’m Bernard Marr, and today I want to dive deep into the transformative trends steering the healthcare landscape in 2024. With technology evolving at a rapid pace, we are venturing into uncharted waters where AI is revolutionizing every facet of healthcare. Generative AI stands tall, making waves in healthcare by democratizing access to transformative AI applications, thereby crafting a personalized healthcare journey for every patient. Personalized medicine is a big buzzword, offering treatment plans crafted down to an individual’s molecular level. By harnessing the power of genomics and AI, we are transitioning into an era of precision medicine, promising better patient outcomes and efficient use of medical resources.
Next up are virtual healthcare assistants—your new companion—facilitating informed healthcare decisions, scheduling appointments, and even offering companionship, bridging the gaps and fostering mental health stability. Imagine having a virtual twin simulating real-time impact of various healthcare scenarios. 2024 seems poised to witness breakthroughs in this space, potentially revolutionizing predictive healthcare. Welcome to telemedicine 2.0, where IoT-powered virtual hospitals are set to take center stage. Imagine virtual hospital wards—a hub where healthcare professionals monitor patients remotely, enhancing the holistic approach to patient care.
Turning our focus towards preventative healthcare, it’s all about being proactive. Technologies are empowering individuals to foster wellness and evade preventative conditions, echoing the wisdom that prevention indeed is better than cure. The realms of VR and AR are melding with healthcare, aiding chronic pain management and offering surgeons real-time digital information, introducing a transformative angle to patient care and treatment. As we witness a surge in the aging population, the spotlight is on innovative solutions that prioritize home care and focus on age-specific ailments, integrating trends like virtual hospitals and preventative care.
Stepping into the revolutionary world of additive manufacturing, where 3D printing is not just about creating tools but venturing into the potential reality of organ transplants, opening avenues to address chronic shortages and reduce procedural costs. Lastly, we are seeing a necessary convergence of mental and physical healthcare, transcending the silos and bringing forth a more holistic approach to health and well-being. As we stand on the brink of these innovations, 2024 beckons with the promise of revolutionized healthcare experiences. Thank you for joining me, Bernard Marr, in exploring the future of healthcare. Remember to like, share, and subscribe for more insights into the world of tomorrow!
Reading
The implementation of Artificial Intelligence in Healthcare
AI makes life simple, allowing us to get rid of mundane, often frustrating tasks. For instance, single calls when a client is being informed about basic procedures. That is why the most down-to-earth applications of artificial intelligence in the medical field regard fulfilling administrative responsibilities. With the help of chatbots providing real-time assistance, patients communicate with AI-driven software to gain the information they need instead of directing their emails straight to reception. 

If you ask anyone about the most desired drug to be developed, most people would probably pick a medicine for cancer treatment. Tulane University, a group of researchers used artificial intelligence to analyze tissue scans to accelerate the process of a colorectal cancer diagnosis. The research involved gathering 13.000 images of colorectal cancer from more than 8.000 subjects from independent medical centers located in Asia, Europe, and the United States. They developed a machine learning model that scored to be more accurate in diagnosis than the human doctors. AI algorithms are able to diagnose cancer more accurately than experienced radiologists do, which brings huge value to the treatment process. Moreover, they can grade the aggressiveness of a rare cancer twice as accurately as a biopsy. As reported by Euronews, Researchers from The Royal Marsden NHS Foundation Trust and The Institute of Cancer Research developed an AI model that is able to accurately predict how aggressive a tumour was likely to be for 82% of them, while only 44% of tumours were correctly graded using a biopsy.

Machine learning can analyze images such as computed tomography (CT) or magnetic resonance imaging (MRI) to track hidden connections and provide crucial data for researchers, hospitals, and their clients. As a result, AI supports radiologists in automating daily administrative tasks, improves diagnostic accuracy, eliminates the risks of human errors, and lets researchers focus on complex cases.

Most medical researchers’ base is, foremost, tissue samples. However, experts’ predictions indicate that thanks to artificial intelligence, an opportunity to invent new medical tools arises. Innovative medical devices are a great example of AI technology used in healthcare regarding imaging tools. Their purpose is to screen chest X-rays in search of tuberculosis or cancer. This idea could be developed further as an app that would give healthcare providers a helpful hand while testing a niche lacking high-quality massive libraries. 

The world is dynamic. More often, it is risk management (of an activity) that poses an essential field to measure rather than the activity itself. It stems from this mentioned dynamic itself as the number of factors to consider increases every year. That is why AI products in healthcare often pertain to accurate risk assessment, for instance: the probability of getting resistance to antibiotics, identifying the suitable layers of risk stratification, or just possibilities for infection. 

Examples of artificial intelligence in healthcare concern not only the scientific side of developing new tools and drugs and accelerating diagnosis processes but also business-related fields such as decision-making. Doctors can gain access to unheard-of insights to obtain a more profound sense of treatment variabilities. This stems from the transparency of the AI line of thinking.

Listening
3D printing. The future of organ transplants

Reporter Gadi: And when it comes to printing human body parts, the future is already here. Just in the last few months, we have seen some pretty incredible results. One woman received a 3-d printed ear plant made from her own cells, as part of a clinical trial. Doctors in France were able to grow a new nose for a cancer patient, using 3-d printed cartilage. And get this, researchers at
M.I.T. can now print 3-d replicas of the human heart. 
Reporter: The team has developed a robotic system that can make soft, 3-d printed replicas of a patient's heart, that can be actuated to mimic the patient's blood pumping ability. The procedure involves first converting medical images of a patient's heart into a three dimensional computer model, which the researchers can then 3-d print using a soft, polymer ink. The result, a soft, flexible shell in the exact shape of the patient's own heart.  Wild, right? Anytime I see something like that, I call nbc news medical fellow, he joins us now. Dr., Why does this matter? What implications does this have on the future of organ transplant?
Dr: Good evening, gadi. The simple way to put it is we don't have enough organs out there for all the people who need organ transplants. Every year, there is about 100,000 people on the organ transplant list and about 17 people die every day waiting for an organ transplant. So, that is why we are seeing a lot of excitement about this, we need a way to solve those organ shortages for transplants, for those that have heart disease, kidney disease. You and I spoke a few weeks ago about a patient who needed a heart transplant and didn't get one. That is why you are seeing the excitement about growing an organ in about as opposed to waiting for an organ to become available.
Reporter Gadi: How does this actually work? Explain the process, we saw the Printing, to physically making a 3-d organ part for the human body?
Dr.: Yeah, it is pretty complicated but I will try to break it down here. Basically, what you do is you take a piece of tissue sample, or a sample of an organ that you want. So, you are in need of a kidney transplant, you can take a piece of that about the size of a postcard and you mix that with a bunch of fancy chemicals and you literally put that into a 3-d printer. So, you think about a color Printer that uses ink to Combine a bunch of colors Together to get the final Product, you are taking a bunch of cells and mixing them together and combining them together and then the 3-d printer layers them on top of each other until you literally get a 3-d printed organ. Gadi, I think the most Important point here to drive Home, because this is coming from a patient sample, you don't need to take those immunosuppressive medications. Those medications that prevent organ transplant rejection. We can actually weaken your immune system and make you more likely to get sick from things like covid.
Reporter Gadi: I was expecting like, an hour long answer and I was ready for it, I was getting ready to sit down and listen to all of it. I don't know how you summed that up in like, two minutes. But I want to know, though, how is this even regulated? This seems like a very brave, new world. How far off are we from seeing this be a huge thing that doctors and hospitals are using on a daily basis?
Reporter: So, the experts really are leading the charge in this, they think about 10 years out is where we are right now. And the organs we are most in need for a transplant right now it is kidney disease. About 90% of patients in need of an organ transplant are waiting for a new kidney. Like you see on the screen there, about 100,000 people waiting for organ transplant. That begs the question, we don't know how it is going to be regulated. I think the really important Thing to drive home is we need to think about ahead of time how we are going to get this to people who need it most. Because going back to the kidney, the people who need it most, over 50% of those waiting for a kidney are minority populations. You want to make sure they are included in the talks to get access to this, as well. And I want to write here, Gadi,

4.	AI in Politics (M4) 

Listening 
"Obama's Political Campaign"

Ladies and gentlemen of Elon University and more specifically ladies and gentlemen of Elon University class of 2018 my name is Morgan Bodenarain and I hope to be the next vice resident of the 2018 class there are a couple things that I intend to do in this next few minutes and there are a couple things that I do not intend to do I do not intend to offer you outlandish and empty promises or a list of changes that I want to pursue once in office however what I do intend to offer you is my time my dedication in my effort previous Student Government involve me involvement has taught me that the most important members of student government are actually the me the students in which we represent your voices fuel our actions I can't offer you flat screen televisions in every dorm Chick-fil-A delivery to your rooms or tater tots every day of the week but what I can offer is my time to listen to all of your concerns and time to do whatever I can to adhere to those concerns I understand that my job as sophomore class VP would be to work for all of you not the other way around as sophomore class vice president the needs of you all are first and foremost before my own agenda essentially your agenda becomes my agenda you tell me what you need and I will do everything in my power to do that upon taking my first steps on Elon's campus I instantly fell in love I knew that I was home when my parents dropped me off in August the thought crossed my mind once again as it has many times after that for the next few years this is our home.

Reading 
"Understanding Campaign Spending Limits"

Social Media use in the 2024 U.S. Presidential Race: A New Campaign Tool or Just a Passing Trend?
In the 2024 U.S. presidential race, TikTok has become a major platform for candidates to reach younger voters. With about one-third of Americans under 30 getting their news from TikTok, candidates are using it to spread their message and take digs at their opponents. Memes, pop culture, and internet slang are common tools in this new era of campaigning. TikTok has around 1 billion active users worldwide, making it a powerful space for political content.
However, this rise in political content on TikTok comes with controversy. Many in Washington, including the candidates, recognize the app as a possible national security threat because it is owned by ByteDance, a company based in China. The U.S. government has already banned TikTok on official devices. In early 2024, President Joe Biden signed a law that could force TikTok to separate from ByteDance or be banned in the U.S. by January 2025. TikTok and ByteDance have sued to block this law, and a decision is expected by the end of the year.
Despite these concerns, presidential candidates are active on TikTok. They have used influencers, memes, and viral trends to attract millions of followers and gain credibility with Generation Z voters. For example, Kamala Harris, Donald Trump, and Robert F. Kennedy Jr. all have significant presences on the platform.
Kamala Harris has two TikTok accounts. One, called @kamalahq, was originally Joe Biden’s campaign account but was transferred to Harris when Biden dropped out of the race. She also created a personal account (@kamalaharris) in July 2024. Her campaign account is known for using popular sounds, memes, and jokes, while her personal account features videos of her at rallies and with celebrities. In one of her most popular videos, Harris challenges Donald Trump to a debate, using the song Not Like Us by Kendrick Lamar to add drama. Harris says that TikTok should not be banned, but she supports changing its ownership.
Like Harris, Donald Trump also has two TikTok accounts: a personal account (@realdonaldtrump) and a campaign account (@teamtrump). Trump uses shorter videos with slogans from his speeches, sometimes featuring influencers like Jake Paul. His campaign account takes a lighter approach, using humor and memes to attract followers. For instance, one post shows dolphins jumping over a rainbow, with the text “Vote for Trump unless you want to be drafted to fight World War III.”
Trump’s views on TikTok have shifted over time. While he once tried to ban the app during his presidency, he now believes that Facebook is a bigger threat to national security and thinks young people would be upset if TikTok disappeared.
Robert F. Kennedy Jr., who initially ran for president before endorsing Trump, has also used TikTok to reach voters. He shares videos that explain his policies, criticize Joe Biden, and promote his environmental ideas. His most popular TikTok video, with 13.8 million views, outlines his campaign promises.
TikTok’s role in the 2024 presidential race shows how much campaigns have changed. It’s not clear yet if being popular on TikTok will result in more votes, especially since younger voters traditionally have lower turnout at the polls. As debates about TikTok’s future in the U.S. continue, it’s clear that the app has changed how political candidates connect with voters. Additionally, LinkedIn platform is also actively used to promote political materials focused on corporate environment. Similarly, Instagram and Twitter are being exploited to engage with a wider range of general population.
This year’s rush of presidential candidates and their running mates to TikTok is redefining the ways political office-seekers interact with key voter bases, despite the backdrop of national security concerns mounted by federal oversight and the candidates themselves. This shift is visible in presidential campaigns of all sizes, including those of third-party candidates Jill Stein and Marianne Williamson. Despite comparatively smaller followings (Stein at 71,600; Williamson at 549,800), content posted to their accounts has still gained traction (Williamson’s account boasts 6.6 million likes). The move to TikTok is a drive to reach America’s youth. Yet whether virality on TikTok translates into votes at the ballot box remains to be seen, especially in a segment of the electorate with historically low voter turnout. As debates rage over the app’s future in the United States, presidential politics may now be an inevitable part of the calculus.

Listening 

"The Role of Technology in Politics"

Major: Perhaps you've noticed, our social media feeds are now a battleground in the race for the white house, and in this space, democrats have deployed influencers to win over voters online.
In tonight's "eye on America," Jo Ling Kent reveals their sophisticated and expensive tactics. 
>>Look at the volume in this hair. 
>>Reporter: 23-year-old Awa Sanneh made a name for herself dispensing beauty tips on TikTok. 
>>I just peed in the white house.
>>Reporter: So when she posted this video of her white house bathroom, her half a million followers took notice.
>> I was just shocked that i like, did you guys see that marble?
>>Reporter: Sanneh, who met us in Houston, was one of a few dozen influencers invited to the white house to watch the state of the union and meet President Biden.
>> He said to us, the collective presence in this room has more viewership on gen Z than all of traditional media combined.
>> So here is my birth control blog.
>> Reporter: This viral video she posted after the fall of roe v. wade... 
>> Over the United States of my uterus.
>> Reporter: that caught the attention of a super pac. on the right, turning point USA has mobilized influencers for years, raising nearly $200 million since 2020.
>> You realize they're coming for you guys next.
>> Reporter: Now democrats are flooding the creator community with cash and providing behind-the-scenes access.
>> Come with me to meet the president of the United States. 
>> We just have to work with them, and if we are not, we are missing a huge way voters are getting in the world.
>> Reporter: Rob Flaherty runs digital strategy, previously at the Biden white house, and now for the Harris campaign. 
>> You think you just fell out of a coconut tree?
>> Reporter: He called the highly meme-able Harris a massive asset as the campaign reaches out to thousands of influencers.
>> Reporter: What kind of coaching do you give influencers acting on behalf of the Harris campaign?
>> Resources, base language.
>> Reporter: While Flaherty said the Harris campaign does not pay influencers directly, CBS news found a constellation of other democratic political organizations that do. in May, future forward, the super Pac supporting Harris, hosted panels like gaming the algorithm and how advocacy can benefit your business. 
>> In the first 100 days of a republican presidency under trump, project 25 talks about thousands of civil servants.
>> Reporter: Last week, prate Sanneh said she was hired by protect our care, and advocacy group that relies on anonymous donors. she made a video warning about trump's second term agenda that most help you script it, right?
>> Right, definitely.
>> Reporter: She takes their talking points and puts them into her own voice, saying she always discloses when she is being paid. What’s your rate?
>> So a video just for a creator of my size, an average can go from $3,000 to $10,000 depending and upwards.
>> This is a bid by campaigns to create authenticity at a small scale.
>> Reporter: University of Pittsburg’s Sam Woolley studies political influencers. How can you tell what is a genuine, grassroots expression of political opinion, versus what's being paid for?
>> If you see multiple influencers spreading the same exact message, you can start to realize, hm, some kind of coordination is going on.
>> Reporter: next up for Sanneh, the democratic national convention.
>> They just told us that if we wanted our own show, that they would give us all the resources to do that.
>> Reporter: Democrats are rolling out the red carpet.
>> Definitely, and I’m glad to be on it.

"""
    result = rate_text_using_gemini(transcription, criteria, course_content)
    save_result_to_file(transcription_file, result)
    print(f"Rating result:\n{result}")
