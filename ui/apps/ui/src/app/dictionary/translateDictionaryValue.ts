import { interoperabilityGuidelinesStatusDictionary } from './interoperabilityGuidelinesStatusDictionary';
import { interoperabilityGuidelinesTypeDictionary } from './interoperabilityGuidelinesTypeDictionary';
import { interoperabilityGuidelinesDomainDictionary } from './interoperabilityGuidelinesDomainDictionary';
import { trainingAccessDictionary } from './trainingAccessDictionary';
import { trainingTargetGroupDictionary } from './trainingTargetGroupDictionary';
import { trainingUrlTypeDictionary } from './trainingUrlTypeDictionary';
import { interoperabilityGuidelinesIdentifierTypeDictionary } from './interoperabilityGuidelinesIdentifierTypeDictionary';
import { DICTIONARY_TYPE_FOR_PIPE } from './dictionaryType';
import { interoperabilityGuidelinesResourceTypeGeneralDictionary } from './interoperabilityGuidelinesResourceTypeGeneralDictionary';
import { interoperabilityGuidelinesAuthorTypeDictionary } from './interoperabilityGuidelinesAuthorTypeDictionary';

export function translateDictionaryValue(
  type: string | string[],
  value: string | string[]
) {
  const valueType: string | string[] = value.toString().toLowerCase();
  switch (type) {
    case DICTIONARY_TYPE_FOR_PIPE.DOMAIN:
      return interoperabilityGuidelinesDomainDictionary[valueType] || value;
      break;
    case DICTIONARY_TYPE_FOR_PIPE.RESOURCE_GENERAL_TYPE:
      return (
        interoperabilityGuidelinesResourceTypeGeneralDictionary[valueType] ||
        value
      );
      break;
    case 'type_general':
      return (
        interoperabilityGuidelinesResourceTypeGeneralDictionary[valueType] ||
        value
      );
      break;
    case DICTIONARY_TYPE_FOR_PIPE.STATUS:
      return interoperabilityGuidelinesStatusDictionary[valueType] || value;
      break;
    case DICTIONARY_TYPE_FOR_PIPE.GUIDELINE_TYPE:
      return interoperabilityGuidelinesTypeDictionary[valueType] || value;
      break;
    case DICTIONARY_TYPE_FOR_PIPE.TRAINING_ACCESS_TYPE:
      return trainingAccessDictionary[valueType] || value;
      break;
    case DICTIONARY_TYPE_FOR_PIPE.TRANING_TARGET_GROUP:
      return trainingTargetGroupDictionary[valueType] || value;
      break;
    case DICTIONARY_TYPE_FOR_PIPE.TRAINING_URL_TYPE:
      return trainingUrlTypeDictionary[valueType] || value;
      break;
    case DICTIONARY_TYPE_FOR_PIPE.IDENTIFIER_TYPE:
      return (
        interoperabilityGuidelinesIdentifierTypeDictionary[valueType] || value
      );
      break;
    case DICTIONARY_TYPE_FOR_PIPE.AUTHOR_TYPE:
      return interoperabilityGuidelinesAuthorTypeDictionary[valueType] || value;
      break;
    default:
      return value;
  }
}
