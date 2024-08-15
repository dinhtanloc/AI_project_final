from libs.common import *
def extract_text_from_html(html_content):

    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator=" ", strip=True)
def process_html_columns(profile_df):

    html_columns = [col for col in profile_df.columns if profile_df[col].astype(str).str.contains('<').any()]

    for col in html_columns:
        profile_df[col] = profile_df[col].apply(extract_text_from_html)

    return profile_df

def row_to_text(row):
    return ". ".join(str(value).replace('\xa0', '') for value in row)

def concat_company_profiles(ticket_collection, clean_html=False):
    all_profiles = pd.DataFrame()

    for i in ticket_collection:
        try:
            company = Vnstock().stock(symbol=i, source='TCBS').company
            profile_df = company.profile()
            if clean_html:
                profile_df = process_html_columns(profile_df)
                

            all_profiles = pd.concat([all_profiles, profile_df], ignore_index=True)
        except:
            print(i)
            continue

    return all_profiles


def concat_company_financial_ratio(ticket_collection):
    all_profiles = pd.DataFrame()

    for i in ticket_collection:
        try:
          print(i)
          stock = Vnstock().stock(symbol=i, source='VCI')
          profile_df = stock.finance.ratio(period='year', lang='en')

          all_profiles = pd.concat([all_profiles, profile_df], ignore_index=True)
        except:
            print(i)
            continue


    return all_profiles


def concat_company_events(ticket_collection):
    all_profiles = pd.DataFrame()
    for i in ticket_collection:
      print(i)
      try:
        company = Vnstock().stock(symbol=i, source='TCBS').company
        profile_df = company.events()
        profile_df.drop(columns=['notify_date',	'exer_date',	'reg_final_date',	'exer_right_date'	], inplace = True)
        profile_df['ticker']=i

        all_profiles = pd.concat([all_profiles, profile_df], ignore_index=True)
      except Exception as e:
        print(f"An error occurred with ticker {i}: {e}")

    return all_profiles



def concat_company_news(ticket_collection):
    all_profiles = pd.DataFrame()
    for i in ticket_collection:
        try:
            company = Vnstock().stock(symbol=i, source='TCBS').company
            print(i)
            profile_df = company.news()
            profile_df["ticker"]=i
        except:
            print(i)
            continue
        all_profiles = pd.concat([all_profiles, profile_df], ignore_index=True)

    return all_profiles





