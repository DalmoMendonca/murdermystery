"""Compile canonical private YAML; generated JSON is compatibility output only."""
import json,yaml
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def write(name,data):
    (ROOT/'source'/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sync():
    design=yaml.safe_load((ROOT/'source/case_design.yaml').read_text(encoding='utf-8'))
    evidence=yaml.safe_load((ROOT/'source/evidence_design.yaml').read_text(encoding='utf-8'))
    write('investigation.json',evidence['reports']);write('discoveries.json',evidence['discoveries'])
    write('case.json',{'revision':design['revision'],'necessary_actions':design['crime']['necessary_actions'],'poisoning_interval':[32,44],'sample_access_interval':[20,28],'critical_discoveries':[14,16],'release_order':design['release_order'],'inference_limit':design['crime']['inference_limit'],'source_routes':design['crime'].get('source_routes',{}),'transport_film':design['crime']['transport_film'],'receiving_seal':design['crime'].get('receiving_seal'),'proof_families':design['proof_families']})
    # The sent public fields are untouched. Compatibility private fields use one loader.
    from character_copy import load_characters
    chars=load_characters();write('characters.json',chars);names={int(c['id']):c['name'] for c in chars}
    specifications={
     'motive':[
      ([1,4,10],'What did Grant demand from you, and what had you already concealed?'),
      ([2,5,8],'What did Grant pressure you to approve or overlook?'),
      ([3,15,17],'What hidden transaction made Grant a threat to you?'),
      ([6,7,22],'How did Grant threaten your work or reputation?'),
      ([9,19,29],'What truth did Grant want suppressed, and what could embarrass you?'),
      ([11,12,26],'What did Grant ask you to hide?'),
      ([13,20,30],'What compromise in your work gave Grant leverage over you?'),
      ([14,18,27],'What did you want returned or protected?'),
      ([16,21,28],'What past agreement was about to become a public dispute?'),
      ([23,24,25],'How did Grant threaten your work, and how did you respond?')],
     'opportunity':[
      ([1,12,29],'What task or errand occupied you before the toast?'),
      ([2,7,17],'How did you approach Grant about your papers or work?'),
      ([3,10,16,21],'When did you first enter, and what business did you have with Grant?'),
      ([4,23,27],'Describe your errand at the private service station.'),
      ([5,20,24],'What physical work or problem occupied you?'),
      ([6,9,15],'What did Grant want changed, and how did you respond before the toast?'),
      ([8,18,19],'Why did you contact the preparation department, and how did you collect your papers?'),
      ([11,13,30],'What practical museum duty were you handling?'),
      ([14,22,28],'What did you bring Grant, and what happened when you delivered it?'),
      ([25,26],'How did your museum materials bring you through the preparation department?')],
     'method':[
      ([2,8,9],'What detail on your paperwork or its packaging should we notice?'),
      ([1,10,30],'What did you handle around the speech or service preparations?'),
      ([3,15,17],'What original record or material completes your account of the dispute?'),
      ([5,20,24],'Which retained record or material explains the work or problem you described?'),
      ([6,7,18],'What physical detail completes your account of the work you wanted protected?'),
      ([4,16,28],'What was on the material you brought, and what does it actually record?'),
      ([11,23,27],'What did your access or service arrangements actually involve?'),
      ([12,22,26],'Which original or retained material did you handle, and what marks does it bear?'),
      ([13,19,25],'What does the completed work or return record tell us?'),
      ([14,21,29],'What retained paper or record supports your account, and what does it disclose?')]
    }
    write('question_rounds.json',[{'key':key,'title':key.title(),'groups':[{'targets':[names[i] for i in ids],'question':q} for ids,q in groups]} for key,groups in specifications.items()])
    print('Compiled evidence, case constraints, private compatibility data, and three regrouped question pages')
if __name__=='__main__':sync()
