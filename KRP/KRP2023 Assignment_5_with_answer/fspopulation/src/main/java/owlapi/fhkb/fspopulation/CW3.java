package owlapi.fhkb.fspopulation;

import java.io.InputStream;
import java.util.Collection;

import org.semanticweb.owlapi.model.IRI;
import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.model.OWLOntologyManager;

import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.util.DefaultPrefixManager;
import org.semanticweb.owlapi.model.OWLIndividual;
import java.util.*;


/**
 * Nanjing University<br>
 * School of Artificial Intelligence<br>
 * KRistal Group<br>
 *
 * Acknowledgement: with great thanks to Nico at Cambridge for the insightful discussions and his useful suggestions in making this project. 
 *
 * This class MUST HAVE A ZERO ARGUMENT CONSTRUCTOR!
 */

public class CW3 {

    private static String NAMESPACE = "http://ai.nju.edu.cn/krp/FamilyHistory#";


    protected CW3() {
        // Do not specify a different constructor to this empty constructor!
    }


    protected void populateOntology(OWLOntologyManager manager, OWLOntology ontology, Collection<JobDataBean> beans) {
        // implement
        OWLDataProperty hasBirthYear = df.getOWLDataProperty(IRI.create(NAMESPACE + "hasBithYear"));
        OWLDataProperty hasYear = df.getOWLDataProperty(IRI.create(NAMESPACE + "hasYear"));
        OWLDataProperty hasGivenName = df.getOWLDataProperty(IRI.create(NAMESPACE + "hasGivenName"));
        OWLDataProperty hasSurname = df.getOWLDataProperty(IRI.create(NAMESPACE + "hasSurname"));
        OWLDataProperty hasMarriedSurname = df.getOWLDataProperty(IRI.create(NAMESPACE + "hasMarriedSurname"));
        OWLDataFactory df = manager.getOWLDataFactory();
        OWLClass person = df.getOWLClass(IRI.create(NAMESPACE + "Person"));
        OWLClass rolePlayed = df.getOWLClass(IRI.create(NAMESPACE + "RolePlayed"));


        String name="";
        for (JobDataBean bean: beans) {
            String surname = bean.getSurname();
            String givenName = bean.getGivenName();
            if (surname==null && surname.length() <= 0) {
                Integer year = bean.getYear();
                String soc = bean.getSource();
                String occupation = bean.getOccupation();
                OWLIndividual tmpRolePlayed = df.getOWLNamedIndividual(IRI.create(NAMESPACE + name + soc + occupation + year.toString()));
                OWLClassAssertionAxiom assertion_axiom = df.getOWLClassAssertionAxiom(person, tmpRolePlayed);
                ontology.add(assertion_axiom);
                OWLDataPropertyAssertionAxiom dataproperty_assertion = df.getOWLDataPropertyAssertionAxiom(hasYear, tmpRolePlayed, year);
                ontology.add(dataproperty_assertion);
            }
            else {
                name = surname+givenName;
                OWLIndividual tmpPerson = df.getOWLNamedIndividual(IRI.create(NAMESPACE + name));
                OWLClassAssertionAxiom assertion_axiom = df.getOWLClassAssertionAxiom(person, tmpPerson);
                ontology.add(assertion_axiom);
                OWLDataPropertyAssertionAxiom dataproperty_assertion = df.getOWLDataPropertyAssertionAxiom(hasSurname, tmpPerson, surname);
                ontology.add(dataproperty_assertion);
                dataproperty_assertion = df.getOWLDataPropertyAssertionAxiom(hasGivenName, tmpPerson, givenName);
                ontology.add(dataproperty_assertion);
                String marriedSurname=bean.getMarriedSurname();
                if (marriedSurname!=null && marriedSurname.length()>0) {
                    dataproperty_assertion = df.getOWLDataPropertyAssertionAxiom(hasMarriedSurname, tmpPerson, marriedSurname);
                    ontology.add(dataproperty_assertion);
                }
                Integer birthYear = bean.getBirthYear();
                if (birthYear!= null) {
                    dataproperty_assertion = df.getOWLDataPropertyAssertionAxiom(hasBirthYear, tmpPerson, birthYear);
                    ontology.add(dataproperty_assertion);
                }
            }
        }
    }

    protected OWLOntology loadOntology(OWLOntologyManager manager, InputStream inputStream) {
        //implement
        OWLOntology owl;
        try {
            owl = manager.loadOntologyFromOntologyDocument(inputStream);
            return owl;
        } catch (OWLOntologyCreationException e) {
            e.printStackTrace();
        }
        return null;
    }

    protected void saveOntology(OWLOntologyManager manager, OWLOntology ontology, IRI locationIRI) {
        // implement
        try {
            manager.saveOntology(ontology, locationIRI);
        } catch (OWLOntologyStorageException e) {
            e.printStackTrace();
        }
    }
}
