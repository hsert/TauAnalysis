/** \class TrackMergeremb
 *
 * 
 * \author Stefan Wayand;
 *         Christian Veelken, LLR
 *
 * \version $Revision: 1.9 $
 *
 * $Id: TrackMergeremb.h,v 1.9 2013/03/23 09:12:51 veelken Exp $
 *
 */

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/Handle.h"




#include <string>
#include <iostream>
#include <map>



template <typename T1>
class TrackMergeremb : public edm::EDProducer 
{
 public:
  explicit TrackMergeremb(const edm::ParameterSet&);
  ~TrackMergeremb();

 private:
  virtual void produce(edm::Event&, const edm::EventSetup&);

  typedef T1 TrackCollectionemb;



  
  //void fill_output_obj(std::auto_ptr<MergeCollection > & output, std::vector<edm::Handle<MergeCollection> > &inputCollections);
  std::string alias_;
  void setAlias(std::string alias){
    alias.erase(alias.size()-6,alias.size());
    alias_=alias;
}

 

};

template <typename T1>
TrackMergeremb<T1>::TrackMergeremb(const edm::ParameterSet& iConfig)
{
 // std::vector<edm::InputTag> inCollections =  iConfig.getParameter<std::vector<edm::InputTag> >("mergCollections");
  //for (auto inCollection : inCollections){
   // inputs_[inCollection.instance()].push_back(consumes<MergeCollection >(inCollection));  
  //}
  //for (auto toproduce : inputs_){
  //  std::cout<<toproduce.first<<"\t"<<toproduce.second.size()<<std::endl;
   // produces<MergeCollection>(toproduce.first);  
  
 //}
  setAlias( iConfig.getParameter<std::string>( "@module_label" ) ); 
  
  produces<TrackCollectionemb>().setBranchAlias( alias_ + "GsfTracks" );
 // produces<reco::TrackExtraCollection>().setBranchAlias( alias_ + "TrackExtras" );
 // produces<reco::GsfTrackExtraCollection>().setBranchAlias( alias_ + "GsfTrackExtras" );
 // produces<TrackingRecHitCollection>().setBranchAlias( alias_ + "RecHits" );
 // produces<std::vector<Trajectory> >() ;
 // produces<TrajGsfTrackAssociationCollection>();
 
 
}

template <typename T1>
TrackMergeremb<T1>::~TrackMergeremb()
{
// nothing to be done yet...  
}


template <typename T1>
void TrackMergeremb<T1>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   
 // for (auto input_ : inputs_){
  //  std::auto_ptr<MergeCollection > output(new MergeCollection());
   // std::vector<edm::Handle<MergeCollection> > inputCollections;
   // inputCollections.resize(input_.second.size());
   // for (unsigned id = 0; id<input_.second.size(); id++){
    //  iEvent.getByToken(input_.second[id], inputCollections[id]);
    // }
   // fill_output_obj(output,inputCollections);   
   // iEvent.put(output,input_.first);
  
//  }
  
    

  
}
